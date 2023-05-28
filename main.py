import shutil
from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Easy Hire"}


@app.post("/uploadresume/")
async def upload_resume(resume: UploadFile):
    file_location = f"resumes/{resume.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
    return {"filename": resume.filename}