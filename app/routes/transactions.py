from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from utils.jwt_handler import get_current_user
from schemas.transaction import TransactionResponse
from models.transaction import Transaction
from models.user import User
from typing import List
from database import get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/", response_model=List[TransactionResponse], status_code=status.HTTP_200_OK)
def get_transactions(
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db),
	wallet_id: int | None = Query(None, description="Фильтр по кошельку")
):
	query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
	print("Initial Query:", query.all())
	if wallet_id:
		query = query.filter(Transaction.wallet_id == int(wallet_id))
	
	transactions = query.order_by(Transaction.updated_at.desc()).all()
	print(transactions)
	return transactions