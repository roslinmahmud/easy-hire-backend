from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    responsibilities = Column(String)
    requirements = Column(String)

    resumes = relationship("Resume", back_populates="job")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    college_name = Column(String)
    email = Column(String)
    phone = Column(String)
    skills = Column(String)
    total_experience = Column(String)
    degree = Column(String)

    job_id = Column(Integer, ForeignKey("jobs.id"))
    job = relationship("Job", back_populates="resumes")
