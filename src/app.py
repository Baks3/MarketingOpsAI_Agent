from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()


drafts_store = []
counter = 1

class Draft(BaseModel):
    email_uid: str
    classification: str
    crm_data: Dict[str, str]
    draft_reply: str
    summary: Dict[str, str]

@app.get("/drafts")
def get_drafts():
    return drafts_store

@app.post("/drafts")
def add_draft(draft: Draft):
    global counter
    draft_entry = {"id": counter, **draft.dict()}
    drafts_store.append(draft_entry)
    counter += 1
    return {"status": "ok", "id": draft_entry["id"]}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html = """
    <html>
    <head>
        <title>Marketing Ops Drafts</title>
    </head>
    <body>
        <h1>Stored Drafts</h1>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>ID</th>
                <th>Email UID</th>
                <th>Classification</th>
                <th>CRM Data</th>
                <th>Summary</th>
                <th>Draft Reply</th>
            </tr>
    """
    for draft in drafts_store:
        html += f"""
        <tr>
            <td>{draft['id']}</td>
            <td>{draft['email_uid']}</td>
            <td>{draft['classification']}</td>
            <td>{draft['crm_data']}</td>
            <td>{draft['summary']}</td>
            <td><pre>{draft['draft_reply']}</pre></td>
        </tr>
        """
    html += """
        </table>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
