import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def enrich_with_crm(subject, sender):
    return {
        "company": "Globex",
        "industry": "Retail",
        "size": "500-1000",
        "contact_role": "Manager"
    }

def classify_email(subject, body):
    if "partnership" in subject.lower() or "inquiry" in body.lower():
        return "Lead Inquiry"
    return "General"

def draft_reply(subject, sender, body):
    prompt = f"Draft a professional reply to {sender} about the following email:\nSubject: {subject}\nBody: {body}\nReply:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content

def process_email(subject, sender, body, uid):
    classification = classify_email(subject, body)
    crm_data = enrich_with_crm(subject, sender)
    draft = draft_reply(subject, sender, body)
    summary = {
        "subject": subject,
        "sender": sender,
        "intent": "business inquiry" if classification == "Lead Inquiry" else "general",
        "urgency": "medium"
    }
    return {
        "email_uid": uid,
        "classification": classification,
        "crm_data": crm_data,
        "draft_reply": draft,
        "summary": summary
    }
