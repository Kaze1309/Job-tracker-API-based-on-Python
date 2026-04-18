from fastapi import APIRouter, HTTPException,status, Depends
from datetime import date
from database import get_session
from sqlalchemy.orm import Session
from db_models import Job
from models import JobCreate
router = APIRouter(
    prefix="/jobs",
)

@router.get("/")
def get_jobs(db: Session = Depends(get_session)):
    jobs_list = db.query(Job).all()
    return {"jobs" : jobs_list}

@router.post("/")
def post_job(job: JobCreate, db: Session = Depends(get_session)):
    new_job = Job(
        company=job.company,
        role=job.role,
        status=job.status,
        job_url= job.job_url,
        date_applied= date.today()
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"message": "job created", "data": new_job}
    
@router.get("/{job_id}")
def get_job(job_id: int, db:Session = Depends(get_session)):
    job_info = db.query(Job).filter(Job.id == job_id).first()
    if job_info != None:
        return {"job": job_info}
    raise HTTPException(status_code=404, detail=f"The job listing for {job_id} does not exist.")
