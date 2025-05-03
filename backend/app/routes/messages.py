from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List


from app.database import get_db

# pydantic models
from app.schemas import MessageCreate, MessageResponse, MessageGenerateRequest

# sqlalchemy models
from app.models import Conversation as ConversationsModel, Message as MessageModel

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
        if len(message_history) <= 1:  # If there is only the user message we just added
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