from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    username: str
    password: str

class Chat(BaseModel):
    username: str
    question: str
    answer: str
    timestamp: datetime
