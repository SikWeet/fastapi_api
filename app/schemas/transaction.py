from datetime import datetime
from pydantic import BaseModel

# ----- Запросы -----
class TransactionRequest(BaseModel):
	from_user_id: int
	from_wallet_id: int
	to_wallet_id: int
	to_user_id: int
	amount: float
	currency: str

# ----- Ответы -----
class TransactionResponse(BaseModel):
    id: int
    wallet_id: int
    to_wallet_id: int
    amount: float
    currency: str
    status: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True