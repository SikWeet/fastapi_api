from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.transaction import Transaction
from schemas.transaction import TransactionRequest as TranRequest

def new_transaction(wallet_id: int, to_wallet_id: int, amount: float, user_id: int, db: Session):
	new_transaction = Transaction(
		wallet_id=wallet_id,
		to_wallet_id=to_wallet_id,
		amount=amount,
		currency="...",
		status="pending",
		user_id=user_id
	)
	db.add(new_transaction)
	db.commit()
	db.refresh(new_transaction)
	return new_transaction

def get_transaction_by_id(transaction_id: int, db: Session):
	transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
	if not transaction:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
	return transaction

def update_transaction_finished(transaction_id: int, status: str, currency: str, db: Session):
	transaction = get_transaction_by_id(transaction_id, db)
	transaction.currency = currency
	transaction.status = status
	db.commit()
	db.refresh(transaction)
	return transaction

def update_transaction_currency(transaction_id: int, currency: str, db: Session):
	transaction = get_transaction_by_id(transaction_id, db)
	transaction.currency = currency
	db.commit()
	db.refresh(transaction)
	return transaction

def update_transaction_status(transaction_id: int, status: str, db: Session):
	transaction = get_transaction_by_id(transaction_id, db)
	transaction.status = status
	db.commit()
	db.refresh(transaction)
	return transaction

def get_transactions_by_wallet_id(wallet_id: int, db: Session):
	transactions = db.query(Transaction).filter(
		(Transaction.wallet_id == wallet_id) | (Transaction.to_wallet_id == wallet_id)
	).all()
	return transactions