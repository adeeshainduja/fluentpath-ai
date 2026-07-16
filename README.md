# 🚀 FluentPath AI – Personal English Communication Coach

An AI-powered English learning platform that helps learners improve their communication skills through personalized practice, intelligent feedback, adaptive learning paths, and learner memory.

---

## 🎥 Demo

▶️ **Watch the Demo Video**

https://youtu.be/8chrDu55LBU

---

# 📖 Overview

FluentPath AI provides an intelligent English learning experience by combining AI-powered evaluations with adaptive coaching. The system remembers learner weaknesses, tracks progress over time, and generates personalized recommendations to improve communication skills.

---

# ✨ Features

## 🔐 Authentication

- User Registration
- Secure Login
- JWT Authentication
- Password Encryption

---

## 📊 Dashboard

- Learning overview
- Practice statistics
- Daily streak
- AI recommendations
- Progress visualization

---

## ✍️ Writing Practice

- Grammar checking
- Vocabulary analysis
- Writing quality assessment
- Personalized feedback
- AI scoring

---

## 🎤 Speaking Practice

- Speech-to-text transcription
- Pronunciation analysis
- Fluency evaluation
- Grammar assessment
- Vocabulary feedback

---

## 📖 Reading Practice

- Reading comprehension
- AI-generated exercises
- Performance tracking

---

## 🎧 Listening Practice

- Listening exercises
- Audio comprehension
- Personalized recommendations

---

## 📚 Vocabulary Practice

- Vocabulary building
- Personalized word suggestions
- Daily practice

---

## 🤖 AI Coach

The AI Coach analyzes learner history and provides:

- Explainable recommendations
- Learning priorities
- Weakness analysis
- Performance summaries
- Strength identification

---

## 🧠 Learning Path

Adaptive learning based on learner performance.

Features include:

- Personalized goals
- Recommended practices
- Current focus area
- Skill progression
- Learning roadmap

---

## 📈 Analytics

- Performance history
- Learning trends
- Average scores
- Progress tracking
- Practice history

---

## 💾 Learner Memory

The platform remembers

- Weak grammar topics
- Vocabulary issues
- Pronunciation mistakes
- Previous practice sessions
- Improvement history

---

# 🏗️ System Architecture

```
                     User
                       │
                       ▼
                React Frontend
                       │
                       ▼
               FastAPI REST API
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
 Authentication   AI Evaluation   Learner Memory
      │                │                │
      └────────────────┼────────────────┘
                       ▼
              Recommendation Engine
                       │
                       ▼
                 PostgreSQL Database
```

---

# 🛠️ Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios

### Backend

- FastAPI
- Python
- SQLAlchemy
- Pydantic
- Uvicorn

### Database

- PostgreSQL

### AI

- Google Gemini API
- Speech Evaluation
- Grammar Analysis
- Adaptive Learning Engine

---

# 📂 Project Structure

```
FluentPath-AI
│
├── frontend
│   ├── src
│   ├── pages
│   ├── components
│   ├── context
│   ├── hooks
│   └── services
│
├── backend
│   ├── app
│   │
│   ├── api
│   ├── core
│   ├── models
│   ├── schemas
│   ├── services
│   ├── memory
│   ├── ai
│   └── utils
│
├── README.md
└── requirements.txt
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/FluentPath-AI.git
```

```
cd FluentPath-AI
```

---

## Backend

```bash
cd backend

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 📸 Screenshots

## Login

![Login](images/login.png)

---

## Dashboard

![Dashboard](images/dashboard.png)

---

## Practice

![Practice](images/practice.png)

---

## Speaking Practice

![Speaking](images/speaking.png)

---

## Learning Path

![Learning Path](images/learning-path.png)

---

## AI Coach

![AI Coach](images/ai-coach.png)

---

# 🔄 Learning Workflow

```
User Practice
      │
      ▼
AI Evaluation
      │
      ▼
Grammar Analysis
Vocabulary Analysis
Pronunciation Analysis
Fluency Analysis
      │
      ▼
Learner Memory Update
      │
      ▼
Adaptive Recommendation
      │
      ▼
Learning Path Generation
      │
      ▼
Progress Tracking
```

---

# 🚀 Future Enhancements

- IELTS Preparation
- TOEFL Practice
- AI Mock Interviews
- Gamification
- Achievement Badges
- Mobile Application
- Real-time Speaking Coach
- Daily Challenges

---

# 👨‍💻 Developer

**Adeesha Induja**

Software Engineering Undergraduate

University of Sri Jayewardenepura

GitHub

https://github.com/adeeshainduja

LinkedIn

https://www.linkedin.com/in/adeesha-induja

---

# 📄 License

This project is developed for educational and research purposes.