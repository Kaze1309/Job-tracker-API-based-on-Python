from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db_models import Note, Job
from database import get_session
from models import NoteCreate


router = APIRouter()
@router.post("/")
def make_note(job_id: int,note: NoteCreate, db: Session = Depends(get_session)):
    job_for_note = db.query(Job).filter(Job.id == job_id).first()
    if job_for_note is None:
        raise HTTPException(status_code=404, detail=f"The job listing for {job_id} not found.")
    new_note = Note(
        content = note.content,
        job_id = job_id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"message":f"note added to job {job_id}"}

@router.get("/")
def get_note(job_id: int, db:Session = Depends(get_session)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail=f"The job for listing {job_id} not found.")

    notes = db.query(Note).filter(Note.job_id == job_id).all()
    if not notes:
        raise HTTPException(status_code=404, detail=f"The notes for job {job_id} not found.")
    return {"message":"note found", "note": notes}


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(job_id: int, note_id:int,db:Session=Depends(get_session)):
    note_to_be_deleted = db.query(Note).filter(Note.id == note_id,Note.job_id == job_id).first()
    if note_to_be_deleted is None:

        raise HTTPException(status_code=404, detail=f"The note for the job listing {job_id} not found.")
    db.delete(note_to_be_deleted)
    db.commit()
 

    