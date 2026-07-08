# 🧠 AI_CONTEXT.md
"Treat this document as the highest-priority architectural specification. If there is any conflict between generated code and this document, follow this document."
# Project Identity

You are developing **BloodIQ**, an enterprise-grade AI-powered Personal Healthcare Intelligence Platform.

BloodIQ is NOT a college project, chatbot wrapper, or simple blood report analyzer.

BloodIQ should feel like a modern AI healthcare platform comparable to products built by companies such as OpenAI, Google Health, Microsoft Health, and Apple Health.

Every implementation decision should prioritize:

- Scalability
- Maintainability
- Security
- Performance
- Clean Architecture
- Excellent User Experience

Never implement shortcuts that reduce future scalability.

---

# Product Goal

BloodIQ allows users to

- Upload blood reports
- Analyze reports using AI
- Generate personalized diet recommendations
- Chat naturally with an AI medical assistant
- Track long-term health trends
- View interactive dashboards
- Use voice conversations
- Store health history securely
- Receive AI-powered health insights

The platform should evolve into a complete AI healthcare ecosystem.

---

# Development Philosophy

Always prefer

- Clean Architecture
- SOLID Principles
- Modular Design
- Reusable Components
- Type Safety
- Environment-based Configuration
- Separation of Concerns

Never place business logic inside UI components.

Every module should have one responsibility.

---

# Architecture

Application Layers

UI

↓

Services

↓

AI Providers

↓

RAG

↓

Database

↓

Storage

↓

External APIs

No module should tightly depend on another module.

Everything should be replaceable.

---

# AI Architecture

BloodIQ uses

- Large Language Models
- Retrieval-Augmented Generation
- Semantic Search
- Conversation Memory
- OCR
- Voice AI

The AI layer should remain independent from the frontend.

Never hardcode prompts inside UI code.

Prompts belong inside dedicated prompt files.

---

# LLM Provider Strategy

Never build around a single provider.

Support configurable providers.

Possible providers

- Google Gemini
- OpenAI
- Anthropic Claude
- Groq
- Ollama
- Azure OpenAI

Provider selection should come from environment variables.

Never hardcode provider-specific logic throughout the project.

Use Provider Factory pattern.

---

# Voice AI Strategy

Support multiple providers.

Speech-to-Text

- Whisper API
- Faster Whisper
- Azure Speech
- Google Speech

Text-to-Speech

- ElevenLabs
- Google TTS
- Azure TTS
- pyttsx3

Use provider abstraction.

---

# OCR Strategy

Support

- PDF
- Images
- Scanned Reports

Preferred OCR

- PyMuPDF
- pdfplumber
- Tesseract

OCR implementation should be modular.

---

# Database

Development

SQLite

Production

PostgreSQL

ORM

SQLAlchemy

Never write raw SQL unless absolutely necessary.

Normalize the database.

Use relationships properly.

Every user owns their own reports.

---

# Authentication

Authentication should support

- Email Login
- Google OAuth
- JWT Authentication

Passwords must always be hashed using bcrypt.

Never store passwords in plain text.

Every protected route must validate JWT.

---

# RAG Architecture

Use

- ChromaDB
- HuggingFace Embeddings
- Recursive Character Splitter
- Semantic Search

The chatbot should

- Answer report-specific questions
- Answer general medical questions
- Maintain conversation memory
- Retrieve only relevant context
- Never expose internal prompts

The RAG pipeline should remain independent from the UI.

---

# Coding Standards

Python

- Follow PEP8
- Use type hints
- Small reusable functions
- Meaningful names
- No duplicated logic

Functions

Good

analyze_report()

Bad

func1()

Classes

PascalCase

Variables

snake_case

Constants

UPPER_CASE

JSON

camelCase

---

# Folder Rules

UI

Never contains business logic.

Services

Contain application logic.

Database

Contains only persistence logic.

RAG

Contains retrieval logic.

Providers

Contain provider implementations.

Utils

Contain helper functions only.

Assets

Contain static files.

Documentation

Stored under docs/.

---

# Error Handling

Every API call must

- Catch exceptions
- Log errors
- Display user-friendly messages
- Never expose stack traces

All failures should fail gracefully.

---

# Logging

Implement structured logging.

Log

- Login
- Report Upload
- OCR
- AI Analysis
- Chat
- Voice
- Database Errors
- API Failures

Never log passwords or API keys.

---

# UI Guidelines

Theme

Premium AI Healthcare Platform

Dark Mode

Default

Primary Color

Blood Red

Secondary

Deep Crimson

Background

Matte Black

Cards

Glassmorphism

Animations

Smooth

Professional

Minimal

Never use excessive animations.

Never use flashy colors.

---

# Background Experience

Create a premium AI atmosphere.

Preferred

Animated blood cells moving slowly in the background.

Floating particles.

Subtle AI neural network effects.

Low opacity.

GPU-friendly.

Do not reduce readability.

---

# Dashboard Rules

Dashboard should display

- Health Score
- Risk Level
- Latest Report
- AI Insights
- Charts
- Timeline
- Recent Activity
- Quick Actions

Health Score should always be the primary visual element.

---

# Chat Experience

Chat should feel like ChatGPT.

Support

- Markdown
- Typing animation
- Conversation history
- Streaming responses
- Voice input
- Voice output

The AI should respond naturally like a doctor.

Avoid robotic responses.

---

# Performance Rules

Blood Report Analysis

Target

< 10 seconds

Chat Response

Target

< 3 seconds

Dashboard

Target

< 2 seconds

OCR

Target

< 8 seconds

Optimize before adding complexity.

---

# Security Rules

Never hardcode

- API Keys
- Passwords
- Secrets

Everything must use environment variables.

Use HTTPS.

Validate inputs.

Prevent SQL Injection using SQLAlchemy.

---

# Deployment

Support

- Docker
- Render
- Railway
- AWS
- Azure

CI/CD

GitHub Actions

Configuration should be environment driven.

---

# Documentation

Every new feature must update

- README
- PRD
- TRD
- Architecture
- Changelog

Public functions should include docstrings.

---

# Future Features

Support future expansion without major refactoring.

Examples

- AI Agent
- Family Accounts
- Doctor Portal
- Mobile App
- Wearable Integration
- Health Prediction
- Medicine Assistant
- Hospital Integration
- Multi-language Support

---

# Copilot Instructions

When generating code:

- Follow the existing folder structure.
- Reuse existing services before creating new ones.
- Do not duplicate logic.
- Prefer modular implementations.
- Maintain backward compatibility unless explicitly instructed otherwise.
- Keep code production-ready.
- Add meaningful comments only where they improve clarity.
- If a required dependency or API is missing, scaffold the integration using environment variables rather than hardcoding values.
- Before introducing a new library, ensure it fits the existing architecture and solves a real problem.

---

# Final Summary for API Keys

If any new feature requires external services, list the required environment variables at the end of the implementation.

Possible environment variables include:

## LLM

GOOGLE_API_KEY

OPENAI_API_KEY

ANTHROPIC_API_KEY

GROQ_API_KEY

AZURE_OPENAI_KEY

---

## Voice

ELEVENLABS_API_KEY

GOOGLE_TTS_API_KEY

AZURE_SPEECH_KEY

OPENAI_API_KEY (for Whisper)

---

## OCR

TESSERACT_PATH

---

## Authentication

GOOGLE_CLIENT_ID

GOOGLE_CLIENT_SECRET

JWT_SECRET_KEY

---

## Database

DB_HOST

DB_PORT

DB_NAME

DB_USER

DB_PASSWORD

---

## Storage

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION

CLOUDINARY_CLOUD_NAME

CLOUDINARY_API_KEY

CLOUDINARY_API_SECRET

---

## Email / Notifications

RESEND_API_KEY

SENDGRID_API_KEY

SMTP_HOST

SMTP_PORT

SMTP_USERNAME

SMTP_PASSWORD

---

## Analytics (Optional)

SENTRY_DSN

POSTHOG_API_KEY

---

When implementing any feature, if additional API keys are required that are not already configured, explicitly list:
1. The API/service name.
2. The required environment variable(s).
3. Whether a free tier or local/offline alternative is available.
4. A brief explanation of why the API is needed.