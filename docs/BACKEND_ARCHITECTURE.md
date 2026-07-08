# 🏗️ Backend Schema, Data Model & Authentication Architecture

# Project

**BloodIQ – AI-Powered Personal Healthcare Intelligence Platform**

---

# 1. Backend Overview

BloodIQ follows a modular, service-oriented backend architecture where each component has a single responsibility. The backend is designed to be scalable, secure, and production-ready.

Core Responsibilities

- User Authentication
- Blood Report Management
- AI Report Analysis
- Diet Recommendation
- AI Medical Chat
- Health Analytics
- Report History
- Notifications
- Voice Processing
- OCR Processing

---

# 2. Backend Architecture

```
                Frontend (Streamlit)

                        │

                        ▼

                FastAPI Backend (Future)

                        │

      ┌─────────────────┼──────────────────┐

      ▼                 ▼                  ▼

Authentication     AI Services       Health Services

      │                 │                  │

      ▼                 ▼                  ▼

PostgreSQL       LangChain + Gemma     ChromaDB

                        │

                        ▼

                HuggingFace Embeddings
```

---

# 3. Database Tables

## Users

| Column | Type |
|---------|------|
| id | UUID |
| full_name | VARCHAR(100) |
| email | VARCHAR(255) UNIQUE |
| password_hash | TEXT |
| profile_image | TEXT |
| age | INTEGER |
| gender | VARCHAR(20) |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

Primary Key

- id

Indexes

- email

---

## Reports

| Column | Type |
|---------|------|
| id | UUID |
| user_id | UUID |
| report_name | VARCHAR |
| report_type | VARCHAR |
| raw_report | TEXT |
| uploaded_file | TEXT |
| report_date | DATE |
| created_at | TIMESTAMP |

Primary Key

- id

Foreign Key

- user_id → Users.id

Indexes

- report_date
- user_id

---

## BloodParameters

Stores every extracted parameter separately.

| Column | Type |
|---------|------|
| id | UUID |
| report_id | UUID |
| parameter | VARCHAR |
| value | VARCHAR |
| unit | VARCHAR |
| reference_range | VARCHAR |
| status | VARCHAR |

Primary Key

- id

Foreign Key

- report_id → Reports.id

Indexes

- parameter
- report_id

---

## DietPlans

| Column | Type |
|---------|------|
| id | UUID |
| report_id | UUID |
| recommendations | JSONB |
| foods_to_eat | JSONB |
| foods_to_avoid | JSONB |
| created_at | TIMESTAMP |

Foreign Key

- report_id

---

## ChatMessages

| Column | Type |
|---------|------|
| id | UUID |
| report_id | UUID |
| role | VARCHAR |
| message | TEXT |
| timestamp | TIMESTAMP |

Indexes

- report_id

---

## HealthScores

| Column | Type |
|---------|------|
| id | UUID |
| report_id | UUID |
| score | INTEGER |
| risk_level | VARCHAR |
| summary | TEXT |

---

## Reminders

| Column | Type |
|---------|------|
| id | UUID |
| user_id | UUID |
| reminder_type | VARCHAR |
| reminder_time | TIMESTAMP |
| status | BOOLEAN |

---

## VoiceSessions

| Column | Type |
|---------|------|
| id | UUID |
| user_id | UUID |
| transcript | TEXT |
| audio_url | TEXT |
| created_at | TIMESTAMP |

---

# 4. Relationships

```
User

│

├──────── Reports

│             │

│             ├──────── Blood Parameters

│             ├──────── Diet Plans

│             ├──────── Chat Messages

│             └──────── Health Score

│

└──────── Reminders

│

└──────── Voice Sessions
```

---

# 5. Database Indexes

Fast lookup required on

Users

- email

Reports

- user_id
- report_date

BloodParameters

- report_id
- parameter

ChatMessages

- report_id

HealthScores

- report_id

---

# 6. Authentication Architecture

Authentication Flow

```
Register

↓

Password Hashing (bcrypt)

↓

PostgreSQL

↓

Login

↓

JWT Token Generated

↓

Protected Routes

↓

Dashboard
```

Supported Authentication

- Email & Password
- Google OAuth
- JWT Access Tokens
- Refresh Tokens (Future)

---

# 7. User Roles

## Guest

Permissions

- View Landing Page
- Register
- Login

Cannot

- Access Reports
- Access Dashboard
- Chat with AI

---

## User

Permissions

- Upload Reports
- AI Analysis
- Generate Diet
- Chat with AI
- Voice Assistant
- View Dashboard
- Delete Own Reports
- Update Profile

Cannot

- View Other Users' Data
- Access Admin Dashboard

---

## Admin

Permissions

- Manage Users
- View System Analytics
- Manage AI Settings
- View Error Logs
- Moderate Reports

---

# 8. Row Level Security

Every user should only access their own records.

Rule

```
Reports.user_id == Current User ID
```

Same applies to

- Chat Messages
- Diet Plans
- Health Scores
- Reminders

No user can query another user's data.

---

# 9. Sensitive Fields

The following fields must never be stored in plain text.

- Password
- JWT Secret
- Google API Key
- OAuth Client Secret

Protected using

- bcrypt
- Environment Variables
- HTTPS

---

# 10. File Storage

Uploads

```
uploads/

    reports/

        user_id/

            report1.pdf

            report2.pdf

    images/

    voice/
```

Future

AWS S3

or

Cloudinary

---

# 11. Event Triggers

Upload Report

↓

OCR

↓

Blood Analysis

↓

Blood Parameter Extraction

↓

Store Parameters

↓

Generate Health Score

↓

Generate Diet

↓

Notify User

---

Generate Diet

↓

Save Diet

↓

Update Dashboard

---

Voice Query

↓

Speech-to-Text

↓

AI Response

↓

Text-to-Speech

↓

Save Transcript

---

# 12. API Endpoints

Authentication

POST /api/auth/register

POST /api/auth/login

POST /api/auth/logout

GET /api/auth/profile

---

Reports

POST /api/reports/upload

GET /api/reports

GET /api/reports/{id}

DELETE /api/reports/{id}

---

Analysis

POST /api/analyze

GET /api/analysis/{id}

---

Diet

POST /api/diet

GET /api/diet/{id}

---

Chat

POST /api/chat

GET /api/chat/history

---

Dashboard

GET /api/dashboard

GET /api/trends

GET /api/health-score

---

Voice

POST /api/voice/transcribe

POST /api/voice/respond

---

OCR

POST /api/ocr/upload

---

Notifications

POST /api/reminders

GET /api/reminders

DELETE /api/reminders/{id}

---

# 13. Security

- Password Hashing using bcrypt
- JWT Authentication
- HTTPS Only
- SQLAlchemy ORM (SQL Injection Protection)
- Environment Variables
- Input Validation using Pydantic
- Secure File Upload Validation
- API Rate Limiting (Future)

---

# 14. Scalability

The backend is designed with independent service modules allowing future migration to microservices without changing the frontend.

Future modules

- AI Agent Service
- OCR Service
- Voice Service
- Notification Service
- Analytics Service
- Doctor Portal
- Mobile API