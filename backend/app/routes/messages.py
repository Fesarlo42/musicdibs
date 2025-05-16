from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List


from app.database import get_db

# pydantic models
from app.schemas import MessageResponse, MessageGenerateRequest

# sqlalchemy models
from app.models import Conversation as ConversationsModel, Message as MessageModel, ProjectGenre, Genre

# services
from app.services.ai_services import GeminiService

router = APIRouter()

@router.get("/for-conversation/{conversation_id}", response_model=List[MessageResponse])
async def get_messages_by_conversation(conversation_id: int, db: Session = Depends(get_db)):
    # Check if conversation exists
    conversation = db.query(ConversationsModel).filter(ConversationsModel.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(MessageModel).filter(MessageModel.conversation_id == conversation_id).order_by(MessageModel.sent_at).all()
    
    return messages


@router.post("/generate", response_model=MessageResponse)
async def generate_ai_message(request: MessageGenerateRequest, db: Session = Depends(get_db)):
    # Check if conversation exists
    conversation = db.query(ConversationsModel).filter(ConversationsModel.id == request.conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
     # Fetch genres associated with the project
    project_genres = db.query(ProjectGenre).filter(
        ProjectGenre.project_id == conversation.project_id
    ).join(Genre).all()
    
    # Format genres as a string
    genres_string = ", ".join([pg.genre.name for pg in project_genres]) if project_genres else "No specific genre"
    
    # Add genres to the conversation object as a transient property
    conversation.genres = genres_string

    # Save user message
    user_message = MessageModel(
        conversation_id=request.conversation_id,
        is_from_ai=False,
        content=request.user_message
    )
    
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # Get message history if any exists
    message_history = db.query(MessageModel).filter(
        MessageModel.conversation_id == request.conversation_id
    ).order_by(MessageModel.sent_at).all()
    
    # Generate AI response
    try:
        try: 
            if len(message_history) <= 1:
                ai_content = await GeminiService.generate_initial_content(
                    conversation, 
                    request.user_message
                )
            else:
                ai_content = await GeminiService.continue_conversation(
                    conversation,
                    message_history,
                    request.user_message
                )
        except Exception as e: 
            raise HTTPException(status_code=502, detail=str(e))

        # Save AI message
        ai_message = MessageModel(
            conversation_id=request.conversation_id,
            is_from_ai=True,
            content=ai_content
        )
        
        db.add(ai_message)
        db.commit()
        db.refresh(ai_message)
        
        return ai_message
        
    except Exception as e:
        # Rollback any changes if there's an error
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))