import shutil

from fastapi import Depends, FastAPI, UploadFile
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/uploadresume/")
async def upload_resume(resume: UploadFile):
    file_location = f"resumes/{resume.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
    return {"filename": resume.filename}


@app.get('/jobs')
def get_jobs(db: Session = Depends(get_db)):
    return crud.get_jobs(db=db)


@app.post('/job', response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db=db, job=job)
