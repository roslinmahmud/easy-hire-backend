from sqlalchemy import Column, ForeignKey, Integer, String, ARRAY
from database import Base
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    responsibilities = Column(ARRAY(String))
    requirements = Column(ARRAY(String))

    resumes = relationship("Resume", back_populates="job")


class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    college_name = Column(ARRAY(String), nullable=True)
    company_names = Column(ARRAY(String), nullable=True)
    degree = Column(ARRAY(String), nullable=True)
    designation = Column(ARRAY(String), nullable=True)
    email = Column(String, nullable=True)
    mobile_number = Column(String, nullable=True)
    name = Column(String, nullable=True)
    no_of_pages = Column(Integer, nullable=True)
    skills = Column(ARRAY(String), nullable=True)
    experience = Column(ARRAY(String), nullable=True)
    total_experience = Column(Integer, nullable=True)
    sort_order = Column(Integer, nullable=True)
    url = Column(String, nullable=True)

    job_id = Column(Integer, ForeignKey("jobs.id"))
    job = relationship("Job", back_populates="resumes")
