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
