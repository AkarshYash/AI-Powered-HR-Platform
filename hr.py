from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/hr", tags=["hr"])

class JobCreate(BaseModel):
    title: str
    department: str
    description: str
    status: str = "Active"

@router.post("/jobs")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = models.Job(**job.model_dump())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()

@router.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.role == "Employee").all()

@router.get("/applicants")
def get_applicants(db: Session = Depends(get_db)):
    # Simple join to get job title and applicant name
    apps = db.query(models.Application, models.Job.title, models.User.name, models.User.email)\
        .join(models.Job, models.Application.job_id == models.Job.id)\
        .join(models.User, models.Application.candidate_id == models.User.id).all()
    
    result = []
    for app, title, name, email in apps:
        result.append({
            "id": app.id,
            "job_title": title,
            "candidate_name": name,
            "candidate_email": email,
            "status": app.status,
            "match_score": app.match_score
        })
    return result

class AppUpdate(BaseModel):
    status: str

@router.put("/applicants/{app_id}")
def update_applicant_status(app_id: int, app_update: AppUpdate, db: Session = Depends(get_db)):
    app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = app_update.status
    db.commit()
    return {"message": "Updated successfully"}
