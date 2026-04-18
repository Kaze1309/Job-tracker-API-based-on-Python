from sqlalchemy import Column, Integer, String, Enum, Date
from models import StatusEnum
from datetime import date
from database import Base

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    company = Column(String)
    role = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.APPLIED)
    date_applied = Column(Date,default=date.today)
    job_url = Column(String)
