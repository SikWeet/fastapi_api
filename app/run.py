from main import app as application
from routes import auth, wallets, transactions
from database import Base, engine

Base.metadata.create_all(bind=engine)

application.include_router(auth.router)
application.include_router(wallets.router)
application.include_router(transactions.router)


if __name__ == "__main__":
	import uvicorn
	uvicorn.run("run:application", host="0.0.0.0", port=8000, reload=True)