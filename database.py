import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import bcrypt

DB_NAME = "nexus_ai.db"

def init_db():
    """Initialize the database tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Chats Table
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  title TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Messages Table
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  chat_id INTEGER NOT NULL,
                  role TEXT NOT NULL,
                  content TEXT NOT NULL,
                  image_data TEXT, -- Base64 image if any
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (chat_id) REFERENCES chats (id))''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- User Functions ---
def create_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    # Hash password using bcrypt
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_pw.decode('utf-8')))
        conn.commit()
        user_id = c.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user:
        stored_hash = user['password_hash'].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return dict(user)
    return None

# --- Chat Functions ---
def create_chat(user_id, title="New Chat"):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO chats (user_id, title) VALUES (?, ?)", (user_id, title))
    conn.commit()
    chat_id = c.lastrowid
    conn.close()
    return chat_id

def get_user_chats(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM chats WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    chats = [dict(row) for row in c.fetchall()]
    conn.close()
    return chats

def save_message(chat_id, role, content, image_data=None):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO messages (chat_id, role, content, image_data) VALUES (?, ?, ?, ?)", 
              (chat_id, role, content, image_data))
    conn.commit()
    conn.close()

def get_chat_history(chat_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM messages WHERE chat_id = ? ORDER BY timestamp ASC", (chat_id,))
    messages = [dict(row) for row in c.fetchall()]
    conn.close()
    return messages

# Initialize on import
init_db()
