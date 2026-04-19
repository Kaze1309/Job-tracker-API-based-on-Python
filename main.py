from router import jobs
from fastapi import FastAPI
from database import engine
from db_models import Base
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(jobs.router)
