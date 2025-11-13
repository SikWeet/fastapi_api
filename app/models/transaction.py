from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Transaction(Base):
	__tablename__ = "transactions"

	id = Column(Integer, primary_key=True, index=True)
	wallet_id = Column(Integer, ForeignKey("wallets.id"))
	to_wallet_id = Column(Integer, nullable=False)
	amount = Column(Integer, nullable=False)
	currency = Column(String, nullable=False)
	status = Column(String, default="pending")
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	user_id = Column(Integer, ForeignKey("users.id"))
	user = relationship("User", back_populates="transactions")
	wallet = relationship("Wallet", back_populates="transactions")