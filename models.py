from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[int] = None
    model_name: Optional[str] = "gemini-2.0-flash"
    persona: Optional[str] = "default" # default, pirate, disney, professional
    image_data: Optional[str] = None # Base64 string

class ChatResponse(BaseModel):
    response: str
    chat_id: int
    timestamp: datetime
