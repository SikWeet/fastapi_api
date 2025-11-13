from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user import User
from models.wallet import Wallet
from schemas.wallet import CreateRequest

def create_wallet(data: CreateRequest, user_id: int, db: Session):
	existing_user = db.query(User).filter(User.id == user_id).first()
	if not existing_user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

	if existing_wallet_by_name(user_id, data.name, db):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Wallet with this name already exists"
		)

	new_wallet = Wallet(user_id=user_id, name=data.name, currency=data.currency)
	db.add(new_wallet)
	db.commit()
	db.refresh(new_wallet)
	return new_wallet

def get_wallets_by_user_id(user_id: int, db: Session):
	wallets = db.query(Wallet).filter(Wallet.user_id == user_id).all()
	if not wallets:
		[]
	return wallets

def get_wallet_by_id(wallet_id: int, user_id: int, db: Session):
	wallet = db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user_id).first()
	if not wallet:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
	return wallet

def get_wallet_only_by_id(wallet_id: int, db: Session):
	wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
	if not wallet:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
	return wallet

def existing_wallet_by_name(user_id: int, name: str, db: Session):
	existing_wallet = (
			db.query(Wallet)
			.filter(Wallet.user_id == user_id, Wallet.name == name)
			.first()
		)
	if existing_wallet:
		return True
	return False