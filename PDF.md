# Marketing Ops AI Agent — README + DESIGN PDF

# 📧 Marketing Ops AI Agent

An AI-powered workflow for Marketing Operations teams.
It monitors emails, classifies them, enriches with CRM data, drafts replies, summarizes content, and stores results via REST.

This repo runs in **live mode**, connecting to a real IMAP inbox and LLM.

---

## 🚀 Quick Start (Live Mode — IMAP + LLM)

### 1. Setup Environment

```bash
python3 -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure `.env`

```ini
IMAP_HOST=imap.gmail.com
IMAP_USER=youraddress@gmail.com
IMAP_PASS=your-app-password   # For Gmail, use an App Password
OPENAI_API_KEY=sk-xxxxxxx
SIGNATURE_NAME="Your Full Name"
```

⚠️ Gmail users → Enable **IMAP** in Gmail settings and generate an **App Password** under *Google Account → Security → App Passwords*.

### 3. Start REST API

```bash
uvicorn src.app:app --reload --host 127.0.0.1 --port 8000
```

### 4. Run IMAP Agent

```bash
python3 src/imap_agent.py
```

The agent will:

* Poll your inbox every 30 seconds
* Process unread emails
* Store results in the REST API

### 5. View Results

#### Browser Dashboard

Open: [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)

#### JSON API

```bash
curl http://127.0.0.1:8000/drafts | jq
```

### Visual Aids

**Pipeline Flowchart**:

```
Incoming Email (IMAP)
        │
        ▼
  IMAP Agent fetches unseen emails
        │
        ▼
  Orchestrator
 ┌───────────────┐
 │ Classifier    │
 │ CRM Enricher  │
 │ Draft Reply   │
 │ Summarizer    │
 └───────────────┘
        │
        ▼
REST API (FastAPI)
  ┌─────────────┐
  │ SQLite DB   │
  │ /drafts API │
  │ /dashboard  │
  └─────────────┘
```

**CRM Mock Table**:

| Email UID | Company  | Industry | Size     | Contact Role |
| --------- | -------- | -------- | -------- | ------------ |
| 8         | Globex   | Retail   | 500-1000 | Manager      |
| 9         | Umbrella | Tech     | 51-200   | Director     |

**Dashboard Wireframe**:

```
+-----------------------------------------------+
| Marketing Ops AI Agent Dashboard              |
+-----------------------------------------------+
| Filter: [All | Lead | Support | General]     |
+-----------------------------------------------+
| Email UID | Sender | Subject       | Status  |
|-----------|--------|---------------|-------- |
| 8         | ...    | Partnership   | Drafted |
| 9         | ...    | API Funding   | Drafted |
+-----------------------------------------------+
```

---

# Design Document — Marketing Ops AI Agent

## Architecture Overview

* **IMAP Agent**: Polls live IMAP inbox, fetches unseen emails.
* **Orchestrator**: Classifies emails, enriches with CRM, drafts replies, and summarizes content.
* **CRM Mock**: Provides company/contact details for enrichment.
* **REST API (FastAPI)**: Stores drafts and JSON summaries in SQLite; exposes `/drafts` and `/dashboard`.
* **LLM Layer**: Uses OpenAI (live) or MockLLM (fallback).

## Chosen Agents

* **Email Classifier**: Categorizes emails (Lead, Support, General, Spam).
* **CRM Enricher**: Attaches company, industry, size, and contact role info.
* **Reply Drafter**: Generates polite, context-aware responses using the LLM.
* **Summarizer**: Produces concise JSON summaries of subject, sender, intent, and urgency.

## Error Handling

* **IMAP Errors**: Retries with exponential backoff.
* **LLM Errors**: Fallback to MockLLM responses.
* **REST API Unavailable**: Queues data locally, retries until successful.
* **Corrupt/Malformed Emails**: Logged and skipped to prevent pipeline crash.
