from pydantic import BaseModel

class ResumeBase(BaseModel):
    email: str
    phone: str
    total_experience: str
    education: str
    skills: str
    about: str
    resume: str

class ResumeCreate(ResumeBase):
    pass    

class Resume(ResumeBase):
    id: int
    job_id: int

    class Config:
        orm_mode = True

class JobBase(BaseModel):
    title: str
    description: str
    responsibilities: str
    requirements: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    resumes: list[Resume] = []

    class Config:
        orm_mode = True

