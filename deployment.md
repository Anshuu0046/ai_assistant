# Deployment Guide 🚀

This project is ready to be deployed! Here are two easy (and free) ways to host your **Magic AI Companion**.

## Option 1: Render (Easiest & Free)

1.  **Push to GitHub**:
    -   Create a new repository on GitHub.
    -   Push this code to it:
        ```bash
        git init
        git add .
        git commit -m "Initial commit"
        git branch -M main
        git remote add origin <your-repo-url>
        git push -u origin main
        ```

2.  **Deploy on Render**:
    -   Go to [dashboard.render.com](https://dashboard.render.com/).
    -   Click **New +** -> **Web Service**.
    -   Connect your GitHub repository.
    -   **Settings**:
        -   **Runtime**: Python 3
        -   **Build Command**: `pip install -r requirements.txt`
        -   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
    -   **Environment Variables**:
        -   Add `GEMINI_API_KEY` with your key.
    -   Click **Create Web Service**.

## Option 2: Docker (For Advanced Users)

1.  **Build the Image**:
    ```bash
    docker build -t magic-ai .
    ```

2.  **Run Locally**:
    ```bash
    docker run -p 8000:8000 -e GEMINI_API_KEY="your_key" magic-ai
    ```

## Important Note on Database
This app uses **SQLite** (`nexus_ai.db`). On free hosting tiers (like Render's free tier), the filesystem is **ephemeral**, meaning your database will reset every time the app restarts.
*   **For a Resume Demo**: This is usually fine.
*   **For Production**: You would want to switch to a hosted PostgreSQL database (Render provides one).
