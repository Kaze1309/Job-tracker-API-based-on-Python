from typing import Optional
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class StatusEnum(str, Enum):
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    REJECTED = "rejected"
    GHOSTED = "ghosted"

class JobCreate(BaseModel):
    company: str
    role: str
    status: StatusEnum = StatusEnum.APPLIED
    job_url: str

class Job(BaseModel):
    job_id: int
    company: str
    role: str
    status: StatusEnum = StatusEnum.APPLIED
    date_applied: date = Field(default_factory=date.today)
    job_url: str

class NoteCreate(BaseModel):
    content: str

class Note(BaseModel):
    note_id: int
    content: str
    time_stamp: date = Field(default_factory=date.today)
class UpdateJobStatus(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[StatusEnum] = None
    job_url: Optional[str] = None
