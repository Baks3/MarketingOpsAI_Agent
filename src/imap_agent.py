import imaplib
import email
import os
import time
import requests
from orchestrator import process_email
from dotenv import load_dotenv

load_dotenv()

IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")
CHECK_INTERVAL = 30  
API_URL = "http://127.0.0.1:8000/drafts"

SIGNATURE_NAME = "[Your Name]"  

def wait_for_api(url):
    while True:
        try:
            requests.get(url)
            print("REST API reachable!")
            break
        except:
            print("Waiting for REST API to start...")
            time.sleep(2)

def fetch_unseen_emails():
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_USER, IMAP_PASS)
    mail.select("inbox")
    typ, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()
    emails = []
    for eid in email_ids:
        typ, msg_data = mail.fetch(eid, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        emails.append((eid.decode(), msg))
    mail.logout()
    return emails

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(errors='ignore')
        return ""
    else:
        return msg.get_payload(decode=True).decode(errors='ignore')

if __name__ == "__main__":
    wait_for_api(API_URL)
    print(f"Starting IMAP agent... polling inbox every {CHECK_INTERVAL} seconds.")
    while True:
        try:
            emails = fetch_unseen_emails()
            for uid, msg in emails:
                subject = msg.get("Subject", "")
                sender = msg.get("From", "")
                body = get_email_body(msg)

                result = process_email(subject, sender, body, uid)

                if isinstance(result, dict) and "draft_reply" in result:
                    draft = result["draft_reply"]
                    if "[Your Name]" in draft:
                        draft = draft.replace("[Your Name]", SIGNATURE_NAME)
                    elif SIGNATURE_NAME not in draft:
                        draft = draft.strip() + f"\n\nBest regards,\n{SIGNATURE_NAME}"
                    result["draft_reply"] = draft

                try:
                    requests.post(API_URL, json=result)
                    print(f"Processed email UID {uid}")
                except requests.exceptions.RequestException as e:
                    print(f"Error sending to REST API: {e}")
        except Exception as e:
            print("Error fetching or processing emails:", e)
        time.sleep(CHECK_INTERVAL)
