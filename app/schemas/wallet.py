from pydantic import BaseModel

# ----- Запросы -----
class CreateRequest(BaseModel):
    name: str
    currency: str

# ----- Ответы -----
class WalletResponse(BaseModel):
    id: int
    user_id: int
    name: str
    balance: float
    currency: str

    class Config:
        orm_mode = True