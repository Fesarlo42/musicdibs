from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from app.database import get_db

# pydantic models
from app.schemas import CreditsBalance, CreditsAdd, CreditsRemove, CreditsList

# sqlalchemy models
from app.models.models import CreditTransaction, User

router = APIRouter()

@router.get("/balance/{user_id}", response_model=CreditsBalance)
def get_credits_balance(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate credits
    credits = db.query(func.sum(CreditTransaction.amount))\
        .filter(CreditTransaction.user_id == user_id, CreditTransaction.type == 'credit')\
        .scalar() or 0
    
    # Calculate debits
    debits = db.query(func.sum(CreditTransaction.amount))\
        .filter(CreditTransaction.user_id == user_id, CreditTransaction.type == 'debit')\
        .scalar() or 0
    
    return {
        "user_id": user_id,
        "total_credits": int(credits - debits)
    } 
    
@router.post("/add", response_model=CreditsBalance)
def add_credits(credit_data: CreditsAdd, db: Session = Depends(get_db)):
    # Verify user exists
    user = db.query(User).filter(User.id == credit_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create credit transaction
    try:
        transaction = CreditTransaction(
            user_id=credit_data.user_id,
            type='credit',
            amount=credit_data.amount
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        current_balance = get_credits_balance(credit_data.user_id, db)
        balance = CreditsBalance(
            user_id=credit_data.user_id,
            total_credits=int(current_balance['total_credits'])
        )
        
        return balance
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error adding credits: {str(e)}"
        )

@router.post("/remove", response_model=CreditsBalance)
def remove_credits(credit_data: CreditsRemove, db: Session = Depends(get_db)):
    # Verify user exists
    user = db.query(User).filter(User.id == credit_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user has enough credits
    current_balance = get_credits_balance(credit_data.user_id, db)
    if isinstance(current_balance, dict) and 'total_credits' in current_balance:
        current_balance = current_balance['total_credits']
        
    if current_balance < credit_data.amount:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient credits. User has {current_balance} credits, but tried to use {credit_data.amount}."
        )

    # Create credit transaction
    try:
        transaction = CreditTransaction(
            user_id=credit_data.user_id,
            type='debit',
            amount=credit_data.amount
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        current_balance = get_credits_balance(credit_data.user_id, db)
        balance = CreditsBalance(
            user_id=credit_data.user_id,
            total_credits=int(current_balance['total_credits'])
        )
        
        return balance
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error removing credits: {str(e)}"
        )

@router.get("/history/{user_id}", response_model=CreditsList)
def get_history(user_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get credit transactions
    all_transactions = db.query(CreditTransaction).filter(CreditTransaction.user_id == user_id)
    total = all_transactions.count()

    transactions = all_transactions.order_by(CreditTransaction.transaction_date.desc()).offset(skip).limit(limit).all()
    
    return CreditsList(
        total=total,
        transactions=transactions,
        page=(skip // limit) + 1,
        limit=limit,
        has_more=(skip + limit) < total
    )