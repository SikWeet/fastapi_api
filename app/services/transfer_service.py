from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from services.wallet_service import get_wallet_by_id, get_wallet_only_by_id

def transfer_funds(wallet_id: int, to_wallet_id: int, amount: float, current_user_id: int, db: Session):
	wallet = get_wallet_by_id(wallet_id, current_user_id, db)
	to_wallet = get_wallet_only_by_id(to_wallet_id, db)
	print(wallet.balance, amount)
	if wallet.balance < amount:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")
	
	if wallet.currency != to_wallet.currency:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Currency mismatch")
	
	wallet.balance -= amount
	to_wallet.balance += amount
	db.commit()
	db.refresh(wallet)
	db.refresh(to_wallet)
	return dict(from_wallet=wallet, to_wallet=to_wallet)

