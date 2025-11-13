from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Wallet(Base):
	__tablename__ = "wallets"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), unique=False)
	name = Column(String, nullable=False)
	balance = Column(Float, default=0.0)
	currency = Column(String, default="USD")

	# обратная связь
	user = relationship("User", back_populates="wallets")
	transactions = relationship("Transaction", back_populates="wallet", cascade="all, delete-orphan")