import shutil
import os

from fastapi import Depends, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/uploadresume/{job_id}")
async def upload_resume(job_id: int, resumes: List[UploadFile]):
    # Create the directory and any intermediate directories
    os.makedirs(f'resumes/{job_id}', exist_ok=True)
    for resume in resumes:
        file_location = f"resumes/{job_id}/{resume.filename}"
        print(file_location)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
    return {"filename": 'yeeeah'}


@app.get('/jobs')
def get_jobs(db: Session = Depends(get_db)):
    return crud.get_jobs(db=db)


@app.post('/job', response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db=db, job=job)


@app.get('/job/{job_id}')
def get_job(job_id: int, db: Session = Depends(get_db)):
    return crud.get_job(db=db, job_id=job_id)


@app.put('/job/{job_id}', response_model=schemas.Job)
def update_job(job_id: int, job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.update_job(db=db, job_id=job_id, job=job)
