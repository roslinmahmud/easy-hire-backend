from sqlalchemy.orm import Session
from sqlalchemy import asc

from pyresparser import ResumeParser
import models, schemas
from nlp_model import get_sorted_candidates


def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resume).offset(skip).limit(limit).all()


def get_resume(db: Session, resume_id: int):
    return db.query(models.Resume).filter(models.Resume.id == resume_id).first()

def delete_resume(db: Session, resume_id: int):
    db.query(models.Resume).filter(models.Resume.id == resume_id).delete()
    db.commit()
    return {"message": "Resume deleted"}


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


def parse_resume(job_id: int, path: str, db: Session):
    data = ResumeParser(path).get_extracted_data()

    data['job_id'] = job_id
    data['sort_order'] = 0
    data['url'] = path
    db_resume = models.Resume(**data)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)


def get_sorted_resumes(job_id: int, db: Session, skip: int = 0, limit: int = 100):
    sort_resumes(job_id, db)
    return db.query(models.Resume).filter(models.Resume.job_id == job_id).order_by(
        asc(models.Resume.sort_order)).offset(skip).limit(limit).all()


def sort_resumes(job_id: int, db: Session):
    db_job = get_job(db, job_id)
    sorted_candidates = get_sorted_candidates(db_job)

    for i in range(len(sorted_candidates)):
        resume = db.query(models.Resume).filter(models.Resume.id == sorted_candidates[i][0]['id']).first()
        if resume is not None:
            resume.sort_order = i
            db.commit()

