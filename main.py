from fastapi import FastAPI
from pyresparser import ResumeParser

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to Easy Hire"}