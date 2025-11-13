from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from services.transaction_service import new_transaction, update_transaction_finished
from services.transfer_service import transfer_funds
from utils.jwt_handler import get_current_user
from schemas.wallet import CreateRequest, WalletResponse
from services.wallet_service import create_wallet, get_wallet_only_by_id, get_wallets_by_user_id, get_wallet_by_id
from models.user import User
from database import get_db

router = APIRouter(prefix="/wallets", tags=["Wallets"])

@router.post("/", response_model=WalletResponse, status_code=status.HTTP_201_CREATED)
def new_wallet(data: CreateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
	return create_wallet(data, current_user.id, db)

@router.get("/", response_model=list[WalletResponse])
def get_wallets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
	return get_wallets_by_user_id(current_user.id, db)

@router.get("/{wallet_id}", response_model=WalletResponse)
def get_wallet(wallet_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
	return get_wallet_by_id(wallet_id, current_user.id, db)

@router.get("/{wallet_id}/transfer", response_model=WalletResponse)
def transfer_money(wallet_id: int, to_wallet_id: int, amount: float, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
	to_wallet = get_wallet_only_by_id(to_wallet_id, db)
	if not to_wallet:
		raise HTTPException(status_code=404, detail="Target wallet not found")
	
	if amount <= 0:
		raise HTTPException(status_code=400, detail="Transfer amount must be positive")
	
	if wallet_id == to_wallet_id:
		raise HTTPException(status_code=400, detail="Cannot transfer to the same wallet")

	transaction = new_transaction(wallet_id, to_wallet_id, -amount, current_user.id, db)
	to_transaction = new_transaction(to_wallet_id, wallet_id, +amount, to_wallet.user_id, db)
	try:
		wallets = transfer_funds(wallet_id, to_wallet_id, amount, current_user.id, db)
		update_transaction_finished(transaction.id, "success", wallets["from_wallet"].currency, db)
		update_transaction_finished(to_transaction.id, "success", wallets["to_wallet"].currency, db)
	except HTTPException as e:
		update_transaction_finished(transaction.id, "failed", "...", db)
		update_transaction_finished(to_transaction.id, "failed", "...", db)
		raise e
	return wallets["from_wallet"]