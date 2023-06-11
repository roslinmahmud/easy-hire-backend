from sqlalchemy.orm import Session
from sqlalchemy import asc
import os

from pyresparser import ResumeParser
import models, schemas


def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resume).offset(skip).limit(limit).all()


def get_resume(db: Session, resume_id: int):
    return db.query(models.Resume).filter(models.Resume.id == resume_id).first()


def get_resume_by_job_id(db: Session, job_id: int):
    return db.query(models.Resume).filter(models.Resume.job_id == job_id).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()


def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()


def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(db: Session, job_id: int, job: schemas.JobCreate):
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not db_job:
        return {"message": "Job not found"}
    db.query(models.Job).filter(models.Job.id == job_id).update(job.dict(exclude_unset=True))
    db.commit()
    return db_job


def get_sorted_resumes(job_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resume).filter(models.Resume.job_id == job_id).order_by(
        asc(models.Resume.sort_order)).offset(skip).limit(limit).all()


def parse_resume(db: Session, job_id, path):
    data = ResumeParser(path).get_extracted_data()

    data['job_id'] = job_id
    # Needs to be fixed
    db_resume = models.Resume(data)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume
