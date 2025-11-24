from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse, UserLogin, UserRegister
from chat_service import chat_service
import database as db
from datetime import datetime
import uvicorn

app = FastAPI(
    title="AI Personal Assistant",
    description="A high-quality full-stack AI assistant project for resume demonstration.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Auth Routes ---
@app.post("/api/auth/register")
async def register(user: UserRegister):
    user_id = db.create_user(user.username, user.password)
    if not user_id:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created", "user_id": user_id}

@app.post("/api/auth/login")
async def login(user: UserLogin):
    user_data = db.verify_user(user.username, user.password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user_data['id'], "username": user_data['username']}

# --- Chat Routes ---
@app.get("/api/chats")
async def get_chats(user_id: int = Header(None)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing User ID")
    return db.get_user_chats(user_id)

@app.post("/api/chats/new")
async def new_chat(user_id: int = Header(None)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing User ID")
    chat_id = db.create_chat(user_id, "New Chat")
    return {"chat_id": chat_id, "title": "New Chat"}

@app.get("/api/chats/{chat_id}/history")
async def get_history(chat_id: int):
    return db.get_chat_history(chat_id)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, user_id: int = Header(None)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing User ID")
    
    # Create chat if not exists
    chat_id = request.chat_id
    if not chat_id:
        chat_id = db.create_chat(user_id, request.message[:30] + "...")
    
    # Save User Message
    db.save_message(chat_id, "user", request.message, request.image_data)
    
    try:
        # Get AI Response
        response_text = chat_service.get_response(
            request.message, 
            request.model_name, 
            request.persona,
            request.image_data
        )
        
        # Save AI Message
        db.save_message(chat_id, "assistant", response_text)
        
        return ChatResponse(
            response=response_text,
            chat_id=chat_id,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_status():
    return {"status": "online", "service": "AI Assistant v2"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
