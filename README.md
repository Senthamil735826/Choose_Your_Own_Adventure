# 🎮 Choose Your Own Adventure

An AI-powered interactive storytelling web application that generates dynamic adventure stories based on a user's chosen theme. Users can explore the generated story, make choices, and experience different story paths.

---

## 🚀 Features

- 🤖 AI-powered story generation using Google Gemini
- 🎭 Interactive choose-your-own-adventure gameplay
- 🌳 Dynamic story branching
- ⚡ FastAPI backend
- ⚛️ React + Vite frontend
- 🗄️ PostgreSQL database support
- 🔄 Background story generation with job status tracking
- 🌐 REST API architecture
- 📱 Responsive user interface
- 🔐 Environment-based API key configuration
- ☁️ GitHub Pages frontend deployment
- ☁️ Vercel backend deployment

---

## 🛠️ Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS
- Axios
- React Router

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- LangChain

### AI

- Google Gemini
- LangChain Google GenAI

### Database

- PostgreSQL
- Neon PostgreSQL

### Deployment

- GitHub
- GitHub Pages
- Vercel

---

## 📁 Project Structure

```text
Choose_Your_Own_Adventure/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── backend/
│   ├── core/
│   │   ├── config.py
│   │   └── story_generator.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │
│   ├── routers/
│   │   ├── story.py
│   │   └── job.py
│   │
│   ├── schemas/
│   │
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── util.js
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── vercel.json
└── README.md
