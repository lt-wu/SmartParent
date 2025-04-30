# SmartParentAssist

**SmartParentAssist** is an AI-powered assistant that helps parents stay on top of school communications. It automatically extracts important dates and event details from school newsletters (including images), updates calendars, and provides an intelligent chatbot to explain events in context.

---

## 📌 Current Workflow

### 1. **Data Ingestion**
- Connects to a mail server to read school newsletters.
- Converts emails to PDF format.
- Uses a **multimodal LLM** (e.g., GPT-4 Vision or Gemini) to extract both text and image-based content.

### 2. **Calendar Updates**
- Extracts event details using a **content parser and summary agent**.
- Applies **user-defined rules** (e.g., event type, timing).
- Sets alarms and schedules actions for upcoming days.
- Syncs with Google Calendar (or similar platforms).

### 3. **Chatbot Interaction**
- Builds a **vector database** for storing structured event data.
- Enables a **chat agent** that can:
  - Answer questions about events.
  - Provide preparation details (e.g., forms, supplies).
  - Explain cultural context (e.g., what is "Spirit Day"?).

---

## 🚀 Future Plan

- **Conflict Warnings** (e.g., overlapping events)
- **Link Parsing** from emails and PDFs
- **Auto Email Replies** based on context
- **Mobile App Development** with notifications

---

## 🧠 System Architecture
