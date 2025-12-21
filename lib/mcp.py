import json
import os
from datetime import datetime
from .domain_model import AuditLogEntry

AUDIT_FILE = "/Users/pewpew/.gemini/antigravity/scratch/fees_explainer_agent/audit.log"
NOTES_FILE = "/Users/pewpew/.gemini/antigravity/scratch/fees_explainer_agent/notes.md"

class MCPClient:
    """
    Handles "Side Effect" actions with Ledger-like auditing.
    """
    
    @staticmethod
    def _log_audit(entry: AuditLogEntry):
        with open(AUDIT_FILE, 'a') as f:
            f.write(entry.model_dump_json() + "\n")
            
    @classmethod
    def save_notes(cls, scenario: str, content: str, content_hash: str, prompt_version: str = "unknown"):
        """Appends to a markdown file."""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"\n## [{timestamp}] Scenario: {scenario}\n{content}\n*(Content Hash: {content_hash})*\n"
        
        with open(NOTES_FILE, 'a') as f:
            f.write(entry)
            
        cls._log_audit(AuditLogEntry(
            actor="user_approved_action",
            action_type="APPEND_NOTES",
            action_payload=json.dumps({"scenario": scenario}),
            content_hash_snapshot=content_hash,
            prompt_version_snapshot=prompt_version
        ))
        return "Notes saved successfully."

    @classmethod
    def draft_email(cls, recipient: str, subject: str, body: str, content_hash: str, prompt_version: str = "unknown"):
        """Simulates drafting an email."""
        # taking a shortcut here to just print for the prototype
        print(f"--- EMAIL DRAFT START ---\nTo: {recipient}\nSubject: {subject}\n\n{body}\n--- EMAIL DRAFT END ---")
        
        cls._log_audit(AuditLogEntry(
            actor="user_approved_action",
            action_type="DRAFT_EMAIL",
            action_payload=json.dumps({"recipient": recipient, "subject": subject}),
            content_hash_snapshot=content_hash,
            prompt_version_snapshot=prompt_version
        ))
        return "Email drafted and logged."
