from typing import Optional
from fastapi import APIRouter, status, HTTPException
from models import Job, JobCreate, Note, NoteCreate, UpdateJobStatus, StatusEnum
from datetime import date
router = APIRouter(
    prefix="/jobs",
)
jobs_list = []
id_count = 1

@router.get("/")
def get_jobs(status_filter: Optional[StatusEnum] = None):
    if status_filter != None:
        by_status = []
        for job in jobs_list:
            if job['status'] == status_filter:
                by_status.append(job)
        return {f"{status_filter.value} jobs": by_status}
    return {"jobs": jobs_list}

@router.post("/",status_code=status.HTTP_201_CREATED)
def post_job(job: JobCreate):
    global id_count
    new_job = {
        "job_id":id_count,
        "company":job.company,
        "role":job.role,
        "status":job.status,
        "job_url": job.job_url,
        "date_applied": date.today()
    }
    jobs_list.append(new_job)
    id_count += 1
    return {"message": "job listed", "data": new_job}

@router.get("/{job_id}", status_code=status.HTTP_200_OK)
def get_job_by_id(job_id: int):
    for job in jobs_list:
        if job['job_id'] == job_id:
            return {"job": job}
    raise HTTPException(status_code=404, detail=f"The job listing {job_id} not found.")

@router.patch("/{job_id}", status_code=status.HTTP_200_OK)
def partial_update_job(job_id:int, job:UpdateJobStatus):
    for index, j in enumerate(jobs_list):
        if j['job_id'] == job_id:
            if job.company is not None:
                jobs_list[index]['company'] = job.company
            if job.role is not None:
                jobs_list[index]['role'] = job.role
            if job.status is not None:
                jobs_list[index]['status'] = job.status
            if job.job_url is not None:
                jobs_list[index]['job_url'] = job.job_url
            return {"message":"job updated", "job":jobs_list[index]}
    raise HTTPException(status_code=404, detail=f"The job listing {job_id} not found.")

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id:int):
    global jobs_list
    for job in jobs_list:
        if job['job_id'] == job_id:
            jobs_list.remove(job)
            return
    raise HTTPException(status_code=404, detail=f"The job listing {job_id} not found.")