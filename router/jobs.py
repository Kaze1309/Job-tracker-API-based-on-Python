from fastapi import APIRouter, HTTPException,status, Depends
from datetime import date
from database import get_session
from sqlalchemy.orm import Session
from db_models import Job
from models import JobCreate, StatusEnum, UpdateJobStatus
from typing import Optional
from router import notes
router = APIRouter(

    prefix="/jobs",
)

#Get jobs by status or All jobs
@router.get("/")
def get_jobs(status_filter: Optional[StatusEnum] = None, db: Session = Depends(get_session)):
    if status_filter != None:
        by_status = db.query(Job).filter(Job.status == status_filter).all()
        return {"filtered_jobs": by_status} 
    return {"jobs" : db.query(Job).all()}

#Post a new job
@router.post("/")
def post_job(job: JobCreate, db: Session = Depends(get_session)):
    new_job = Job(
        company=job.company,
        role=job.role,
        status=job.status,
        job_url= job.job_url
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"message": "job created", "data": new_job}

#get a job by job id 
@router.get("/{job_id}")
def get_job(job_id: int, db:Session = Depends(get_session)):
    job_info = db.query(Job).filter(Job.id == job_id).first()
    if job_info != None:
        return {"job": job_info}
    raise HTTPException(status_code=404, detail=f"The job listing for {job_id} does not exist.")

#update fields of a job
@router.patch("/{job_id}")
def partial_update_job(job_id: int,job: UpdateJobStatus, db:Session = Depends(get_session)):
    job_to_be_updated = db.query(Job).filter(Job.id == job_id).first()
    if job_to_be_updated is None:
        raise HTTPException(status_code=404, detail=f"The job listing for {job_id} does not exist.")
    if job.company is not None:
        job_to_be_updated.company = job.company
    if job.role is not None:
        job_to_be_updated.role = job.role
    if job.status is not None:
        job_to_be_updated.status = job.status
    if job.job_url is not None:
        job_to_be_updated.job_url = job.job_url
    db.commit()
    db.refresh(job_to_be_updated)

    return {"message": "job updated", "job": job_to_be_updated}


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db:Session = Depends(get_session)):
    job_to_be_deleted = db.query(Job).filter(Job.id == job_id).first()
    if job_to_be_deleted is None:
        raise HTTPException(status_code=404, detail=f"The job listing for {job_id} does not exist.")
    db.delete(job_to_be_deleted)
    db.commit()
    return {"message": "job deleted"} 
 
router.include_router(notes.router, prefix="/{job_id}/notes")