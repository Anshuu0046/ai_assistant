# Nexus AI - Personal Assistant

A high-performance, full-stack AI Personal Assistant application built with **FastAPI** and **Modern Vanilla JavaScript**. Designed to demonstrate scalable architecture, real-time API interaction, and premium UI/UX design.

![Project Screenshot](https://via.placeholder.com/800x400?text=Nexus+AI+Dashboard)

## 🚀 Key Features

- **High-Performance Backend**: Built on [FastAPI](https://fastapi.tiangolo.com/) for asynchronous request handling and automatic documentation.
- **Modern UI/UX**: Custom-designed interface using [Tailwind CSS](https://tailwindcss.com/) with dark mode, glassmorphism effects, and responsive layout.
- **Real-Time Interaction**: Seamless chat experience with typing indicators and instant feedback.
- **Extensible Architecture**: Modular design (Service-Repository pattern) allowing easy integration of LLMs like OpenAI GPT-4 or Gemini.

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, FastAPI, Uvicorn, Pydantic
- **Frontend**: HTML5, Vanilla JavaScript (ES6+), Tailwind CSS
- **Tools**: Git, Docker (ready)

## 📦 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nexus-ai.git
   cd nexus-ai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the App**
   Open your browser and navigate to `http://localhost:8000`.

## 💡 How It Works

- The **Frontend** sends asynchronous `POST` requests to `/api/chat`.
- The **Backend** (`main.py`) validates data using Pydantic models (`models.py`).
- The **Service Layer** (`chat_service.py`) processes the input (currently using a keyword-based mock engine, ready for LLM API injection) and returns a structured response.

## 🔮 Future Improvements

- [ ] Integrate OpenAI API for real generative AI.
- [ ] Add database (PostgreSQL) to save chat history.
- [ ] Implement user authentication (OAuth2).

---
*Built by [Your Name] for [Target Role]*
