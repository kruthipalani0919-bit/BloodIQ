# 🩸 BloodIQ – Application Flow Document

Version: 1.0

---

# 1. Product Overview

BloodIQ is an AI-powered Personal Healthcare Intelligence Platform that enables users to analyze blood reports, monitor long-term health trends, receive personalized health recommendations, and interact with an intelligent AI medical assistant through text and voice.

The application is designed around a modular healthcare workflow that transforms medical reports into meaningful health insights.

---

# 2. Entry Point

When a user launches the application, they are directed to the Authentication Screen.

```
Launch Application
        │
        ▼
Authentication
        │
        ▼
Dashboard
```

---

# 3. Navigation Structure

The application uses a persistent left sidebar for primary navigation.

```
Sidebar

🏠 Dashboard

📄 Blood Reports

📊 Health Analytics

🤖 AI Doctor

🎤 Voice Assistant

📅 Health Timeline

🔔 Reminders

👤 Profile

⚙ Settings

🚪 Logout
```

The selected page remains highlighted.

Navigation never loses user context.

---

# 4. Authentication Flow

```
Open App

↓

Welcome Screen

↓

Login

OR

Create Account

↓

Email Verification

↓

Profile Setup

↓

Health Preferences

↓

Dashboard
```

Supported Authentication

- Email & Password
- Google Sign-In
- Forgot Password
- Password Reset

---

# 5. Onboarding Flow

First-time users complete a short onboarding process.

Step 1

Basic Information

- Name
- Age
- Gender

↓

Step 2

Health Profile

- Existing Conditions
- Allergies
- Current Medications

↓

Step 3

Lifestyle

- Activity Level
- Diet Preference
- Water Intake Goal

↓

Dashboard

---

# 6. Dashboard

The Dashboard serves as the central hub.

Displays

- Health Score
- Latest Blood Report
- Health Trends
- AI Insights
- Upcoming Reminders
- Recent Conversations
- Quick Actions

Quick Actions

- Upload Report
- Talk to AI Doctor
- Voice Assistant
- View Dashboard
- Generate Diet Plan

---

# 7. Blood Report Workflow

```
Dashboard

↓

Upload Report

↓

Select Input Method

├── PDF

├── Image

└── Manual Text

↓

OCR Processing

↓

AI Blood Analysis

↓

Parameter Extraction

↓

Health Summary

↓

Health Score

↓

Save Report

↓

Dashboard Updated
```

---

# 8. AI Analysis Workflow

```
Blood Report

↓

Gemma LLM

↓

Blood Parameter Extraction

↓

Reference Range Comparison

↓

High / Low Detection

↓

Patient Summary

↓

Risk Assessment

↓

Health Score

↓

Store Results
```

---

# 9. Personalized Diet Flow

```
Completed Analysis

↓

Generate Diet

↓

AI Nutrition Engine

↓

Foods to Eat

↓

Foods to Avoid

↓

Lifestyle Suggestions

↓

Weekly Meal Plan

↓

Save Diet Plan
```

---

# 10. AI Doctor Workflow

```
Dashboard

↓

Open AI Doctor

↓

User Question

↓

Conversation Memory

↓

Need Blood Report Context?

YES
↓

RAG Retrieval

↓

Relevant Report Chunks

↓

Gemma LLM

↓

Medical Response

↓

Save Conversation
```

If no report context is required

```
Question

↓

Gemma Medical Knowledge

↓

Response
```

---

# 11. Voice Assistant Workflow

```
Open Voice Assistant

↓

Speech Input

↓

Speech-to-Text

↓

Intent Detection

↓

RAG + LLM

↓

Answer

↓

Text-to-Speech

↓

Voice Response
```

---

# 12. Health Dashboard Workflow

```
Dashboard

↓

View Trends

↓

Select Parameter

↓

Historical Reports

↓

Generate Charts

↓

AI Insights

↓

Recommendations
```

Supported Parameters

- Hemoglobin
- WBC
- Platelets
- Cholesterol
- Blood Sugar
- Vitamin D
- Iron
- Thyroid

---

# 13. Health Timeline Workflow

```
Timeline

↓

Monthly Reports

↓

AI Comparison

↓

Trend Detection

↓

Health Progress
```

---

# 14. Reminder Workflow

```
Dashboard

↓

Create Reminder

↓

Medicine

OR

Water

OR

Exercise

OR

Blood Test

↓

Notification Scheduled
```

---

# 15. Profile Workflow

```
Profile

↓

View Information

↓

Edit Details

↓

Update Preferences

↓

Save Changes
```

---

# 16. Settings Workflow

Users can configure

- Theme
- Notification Preferences
- Voice Language
- AI Response Style
- Privacy Settings
- Connected Devices

---

# 17. Primary User Journeys

## Journey 1

New User

```
Launch App

↓

Register

↓

Complete Profile

↓

Upload Blood Report

↓

AI Analysis

↓

Generate Diet

↓

Talk with AI Doctor

↓

Dashboard
```

---

## Journey 2

Returning User

```
Login

↓

Dashboard

↓

View Health Trends

↓

Upload New Report

↓

Compare Reports

↓

Updated Health Score
```

---

## Journey 3

Voice Interaction

```
Login

↓

Voice Assistant

↓

Speak Question

↓

AI Analysis

↓

Voice Response
```

---

# 18. Redirect Logic

| User Action | Redirect |
|-------------|----------|
| Successful Login | Dashboard |
| Registration Complete | Onboarding |
| Onboarding Complete | Dashboard |
| Upload Successful | Analysis Screen |
| Analysis Complete | Dashboard |
| Generate Diet | Diet Screen |
| Open AI Doctor | Chat Interface |
| Logout | Login Screen |

---

# 19. Loading States

Display loading indicators during

- OCR Processing
- Blood Analysis
- Diet Generation
- Chat Response
- Dashboard Loading
- Report Upload
- Voice Processing

---

# 20. Empty States

Examples

No Reports

"Upload your first blood report to begin your health journey."

No Conversations

"Start a conversation with the AI Doctor."

No Dashboard Data

"Complete your first analysis to unlock health insights."

No Diet Plan

"Generate your personalized nutrition plan."

---

# 21. Error States

- Invalid Report Format
- OCR Failure
- AI Service Unavailable
- Network Connection Lost
- Authentication Failed
- Database Connection Error
- Unsupported File Type
- Empty Report Submission

Each error should provide a clear explanation and recovery action.

---

# 22. Modal & Overlay Interactions

Confirmation Modals

- Delete Report
- Logout
- Delete Account

Upload Modal

- Choose Upload Type
- PDF
- Image
- Manual Input

Voice Assistant Overlay

- Listening Animation
- Processing Indicator
- Speaking Animation

Loading Overlay

- AI Analysis Progress
- OCR Progress
- Report Upload Progress

---

# 23. Notifications

In-App Notifications

- Report Successfully Saved
- Analysis Completed
- Diet Plan Generated
- Reminder Created
- Login Successful

System Notifications

- Medicine Reminder
- Water Reminder
- Exercise Reminder
- Blood Test Due

---

# 24. Application Exit Flow

```
Logout

↓

Clear Session

↓

Secure Token Removal

↓

Redirect to Login
```

---

# 25. Complete Application Flow

```
Launch Application

↓

Authentication

↓

Onboarding

↓

Dashboard

↓

Upload Blood Report

↓

OCR

↓

AI Analysis

↓

Health Score

↓

Diet Recommendation

↓

AI Doctor

↓

Voice Assistant

↓

Health Dashboard

↓

Health Timeline

↓

Reminders

↓

Profile

↓

Settings

↓

Logout
```

---

# Flow Design Principles

- Minimal navigation depth
- Context-aware AI interactions
- Persistent conversation history
- Secure user-specific data
- Modular architecture
- Scalable healthcare workflow
- Responsive user experience
- AI-first design philosophy