from router import jobs
from fastapi import FastAPI

app = FastAPI()
app.include_router(jobs.router)