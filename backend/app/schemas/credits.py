from pydantic import BaseModel
from typing import Literal, Optional, List
from datetime import datetime

# Credits models
class CreditBase(BaseModel):
    user_id: int
    amount: int

class CreditsAdd(CreditBase):
    pass

class CreditsRemove(CreditBase):
    pass

class CreditTransaction(CreditBase):
    id: int
    type: Literal["credit", "debit"]
    transaction_date: datetime
    
    class Config:
        from_attributes = True

class CreditsBalance(BaseModel):
    user_id: int
    total_credits: int

class CreditsList(BaseModel):
    total: int
    transactions: List[CreditTransaction]
    page: int
    limit: int
    has_more: bool
