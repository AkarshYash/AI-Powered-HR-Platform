from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models

# Import ML logic
from ml.resume_screener import calculate_resume_score
from ml.chatbot import get_chatbot_response

router = APIRouter(prefix="/ai", tags=["ai"])

class ResumeScreenRequest(BaseModel):
    application_id: int
    resume_text: str

class ChatRequest(BaseModel):
    message: str

@router.post("/screen-resume")
def screen_resume(req: ResumeScreenRequest, db: Session = Depends(get_db)):
    # Fetch application
    app = db.query(models.Application).filter(models.Application.id == req.application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    # Find job description
    job = db.query(models.Job).filter(models.Job.id == app.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Associated Job not found")
        
    # Calculate score
    result = calculate_resume_score(req.resume_text, job.description)
    score = result["score"]
    missing = result["missing_keywords"]
    
    # Update application
    app.resume_text = req.resume_text
    app.match_score = score
    db.commit()
    
    return {"match_score": score, "missing_keywords": missing, "message": "Resume screened successfully"}

@router.post("/chat")
def chat_with_bot(req: ChatRequest):
    response = get_chatbot_response(req.message)
    return {"response": response}
