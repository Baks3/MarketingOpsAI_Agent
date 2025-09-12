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

Example output:

```json
[
  {
    "id": 1,
    "email_uid": "42",
    "classification": "Lead Inquiry",
    "crm_data": {
      "company": "Umbrella",
      "industry": "Retail",
      "size": "51-200",
      "contact_role": "Manager"
    },
    "draft_reply": "Dear John Doe,\n\nThank you for reaching out ...\n\nBest regards,\nTsepang Mabizela",
    "summary": {
      "subject": "Partnership request",
      "sender": "john@acme.com",
      "intent": "business inquiry",
      "urgency": "medium"
    }
  }
]
```

---

## 🔄 Extensibility

* Swap LLM providers → `src/llm_providers.py`
* Expand CRM → `src/crm_mock.py`
* Change storage → `src/app.py`
* Add new classifiers → `src/orchestrator.py`

---

## 🛡 Error Handling

* IMAP errors → retry with backoff
* LLM errors → fallback to mock
* REST offline → queue + retry later
* Corrupt emails → logged + skipped

---

## 📄 Docs

* `DESIGN.md` → one-page architecture & error handling overview
