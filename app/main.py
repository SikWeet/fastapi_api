from fastapi import FastAPI
from database import Base, engine

app = FastAPI(title="My FastAPI Application", version="1.0.0")