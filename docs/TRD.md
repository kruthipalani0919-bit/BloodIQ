# 🛠 Technical Requirements Document (TRD)

# Project

**BloodIQ – AI-Powered Personal Healthcare Intelligence Platform**

Version: 2.0

---

# 1. Technical Vision

BloodIQ is designed as a modular, AI-first healthcare platform that combines Artificial Intelligence, Retrieval-Augmented Generation (RAG), Health Analytics, Voice AI, OCR, and secure cloud infrastructure.

The system must support replacing AI providers, databases, authentication providers, and deployment platforms with minimal code changes.

---

# 2. Core Technology Stack

## Frontend

- Streamlit (Current)
- React + Next.js (Future Web Portal)
- HTML5
- CSS3
- JavaScript
- Plotly
- Streamlit Components

---

## Backend

Current

- Python

Future

- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy

---

## Database

Development

- SQLite

Production

- PostgreSQL

ORM

- SQLAlchemy ORM

---

## AI Layer

Framework

- LangChain (LCEL)

Capabilities

- Prompt Engineering
- Structured Output
- Conversation Memory
- Agent Workflow
- Tool Calling

---

## RAG

Vector Database

- ChromaDB

Embeddings

- HuggingFace Sentence Transformers

Model

- all-MiniLM-L6-v2

Retrieval

- Semantic Search
- Similarity Search
- Context Retrieval

---

# 3. AI Provider Architecture

The application must never depend on a single LLM provider.

Supported Providers

- Google Gemini
- OpenAI GPT
- Anthropic Claude
- Groq
- Ollama
- Azure OpenAI

Provider selection must be configurable using environment variables.

```
LLM_PROVIDER=gemini
```

The implementation should use a Provider Factory pattern so changing providers requires only configuration changes.

---

# 4. Voice AI Architecture

Speech-to-Text Providers

- OpenAI Whisper API
- Faster-Whisper (Offline)
- Azure Speech
- Google Speech API

Text-to-Speech Providers

- ElevenLabs
- Google Text-to-Speech
- Azure TTS
- pyttsx3 (Offline)

Voice provider selection must also be configurable.

---

# 5. OCR Architecture

Supported Providers

- PyMuPDF
- pdfplumber
- Tesseract OCR

Supported Inputs

- PDF
- Image
- Scanned Documents

---

# 6. Authentication

Supported Authentication Methods

- Email & Password
- Google OAuth
- GitHub OAuth
- Microsoft OAuth

Security

- JWT Access Tokens
- Refresh Tokens
- Password Hashing (bcrypt)
- Session Management

---

# 7. Deployment

Development

- Local Environment

Production

- Docker
- Render
- Railway
- AWS
- Azure

CI/CD

- GitHub Actions

---

# 8. Third-Party Services

AI

- Google Gemini
- OpenAI
- Claude
- Groq

Voice

- ElevenLabs
- Google TTS

Speech Recognition

- Whisper

OCR

- Tesseract

Charts

- Plotly

Notifications

- Email Service
- Push Notifications

---

# 9. Folder Structure

```
bloodiq/

├── app.py

├── database/
│   ├── connection.py
│   ├── models.py
│   ├── crud.py
│   └── migrations/

├── rag/
│   ├── rag.py
│   ├── retriever.py
│   ├── embeddings.py
│   └── prompts.py

├── services/
│   ├── analysis_service.py
│   ├── diet_service.py
│   ├── chat_service.py
│   ├── auth_service.py
│   ├── voice_service.py
│   ├── ocr_service.py
│   ├── notification_service.py
│   └── dashboard_service.py

├── providers/
│   ├── llm_factory.py
│   ├── voice_factory.py
│   ├── ocr_factory.py
│   └── auth_factory.py

├── models/

├── utils/

├── assets/

├── uploads/

├── docs/

├── .env

└── requirements.txt
```

---

# 10. Environment Variables

## LLM

```
LLM_PROVIDER=
GOOGLE_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GROQ_API_KEY=
AZURE_OPENAI_KEY=
```

---

## Voice

```
VOICE_PROVIDER=

ELEVENLABS_API_KEY=

GOOGLE_TTS_API_KEY=

AZURE_SPEECH_KEY=
```

---

## OCR

```
OCR_PROVIDER=

TESSERACT_PATH=
```

---

## Authentication

```
JWT_SECRET_KEY=

GOOGLE_CLIENT_ID=

GOOGLE_CLIENT_SECRET=

GITHUB_CLIENT_ID=

GITHUB_CLIENT_SECRET=
```

---

## Database

```
DB_HOST=

DB_PORT=

DB_NAME=

DB_USER=

DB_PASSWORD=
```

---

## Storage

```
STORAGE_PROVIDER=

AWS_ACCESS_KEY=

AWS_SECRET_KEY=

CLOUDINARY_API_KEY=
```

---

# 11. Naming Conventions

Files

- snake_case

Classes

- PascalCase

Variables

- snake_case

JSON Keys

- camelCase

Database Tables

- plural lowercase

Services

- One Responsibility Per File

---

# 12. Technical Constraints

- Modular Architecture
- Environment-based Configuration
- No Hardcoded Secrets
- Independent AI Services
- Provider Factory Pattern
- SQLAlchemy ORM
- Stateless Backend
- Secure Authentication
- Scalable Service Layer
- Replaceable AI Providers

---

# 13. Performance Targets

Blood Report Analysis

< 10 seconds

Chat Response

< 3 seconds

Voice Response

< 4 seconds

OCR

< 8 seconds

Dashboard

< 2 seconds

---

# 14. Development Standards

- Type Hints
- PEP8
- Modular Code
- Reusable Components
- Comprehensive Error Handling
- Logging
- Environment-based Configuration
- Dependency Injection where applicable
- Clean Architecture Principles

---

# 15. Future Scalability

The backend must support future modules without major architectural changes.

Planned Modules

- AI Agent
- Doctor Portal
- Family Accounts
- Mobile API
- Wearable Integration
- Health Prediction Engine
- Appointment Booking
- Medical Report Sharing
- Cloud Sync
- Multi-language Support