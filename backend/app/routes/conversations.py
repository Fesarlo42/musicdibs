from fastapi import APIRouter, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db

# pydantic models
from app.schemas import ConversationCreate, ConversationResponse, ConversationDetailResponse

# sqlalchemy models
from app.models import Conversation as ConversationsModel, Message as MessageModel, File as FileModel

# services
from app.services.ai_services import GeminiService
from app.services.files_services import upload_generated_file, get_presigned_url

router = APIRouter()

@router.post("", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate, 
    db: Session = Depends(get_db)
):
    db_conversation = ConversationsModel(
        project_id=conversation.project_id,
        purpose=conversation.purpose,
        tempo=conversation.tempo,
        key_signature=conversation.key_signature,
        mood=conversation.mood
    )
    
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    
    return db_conversation


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(ConversationsModel).filter(ConversationsModel.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation


@router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = db.query(ConversationsModel).filter(ConversationsModel.id == conversation_id).first()
    
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(db_conversation)
    db.commit()
    
    return Response(status_code=204)


@router.post("/{conversation_id}/finish", status_code=200)
async def finish_conversation(
    conversation_id: int, 
    db: Session = Depends(get_db)
):
    conversation = db.query(ConversationsModel).filter(ConversationsModel.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(MessageModel).filter(MessageModel.conversation_id == conversation_id).order_by(MessageModel.sent_at).all()
    
    if not messages:
        raise HTTPException(status_code=400, detail="No messages to export")
    
    file_content = await GeminiService.export_to_file(conversation, messages)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"music_conversation_{conversation_id}_{timestamp}.txt"
    
    # upload to minio
    try:
        object_key = upload_generated_file(file_content, filename)

        # Link the file to a project
        db_file = FileModel(
            project_id=conversation.project_id,
            object_key=object_key,
            name=filename,
            origin="ai_generated"
        )

        db.add(db_file)

        # finish conversastion
        conversation.status = "completed"

        db.commit()
        db.refresh(db_file)

        return {
            "status": "success",
            "file_id": db_file.id,
            "filename": db_file.name,
            "download_url": get_presigned_url(object_key, db_file.name)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export and upload conversation: {str(e)}"
        )
