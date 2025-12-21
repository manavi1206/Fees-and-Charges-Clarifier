import hashlib
from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, AnyHttpUrl

# ==========================================
# Enums & Constants (The "Registry" Types)
# ==========================================

class IntentType(BaseModel):
    """Registry of allowed intents. Anything else is blocked."""
    # Added TAXATION and TRANSACTION_LIMITS based on user dataset analysis
    name: str = Field(..., pattern=r"^(EXIT_LOAD|SIP_CHARGES|STAMP_DUTY|EXPENSE_RATIO|OIRC_CHARGES|TRANSACTION_CHARGES|TAXATION|TRANSACTION_LIMITS)$")

class RefusalReason(BaseModel):
    reason_code: Literal["COMPARISON", "ADVICE", "PERFORMANCE", "HYPOTHETICAL", "UNKNOWN_SOURCE", "PII", "OUT_OF_SCOPE", "UNDOCUMENTED_FEE"]
    regulatory_message: str

# ==========================================
# Data Contracts (Workflow Inputs/Outputs)
# ==========================================

class UserQuery(BaseModel):
    """Input from the User."""
    raw_query: str = Field(..., min_length=5, max_length=500)
    user_id: str = Field(default="anonymous")
    force_refresh: bool = Field(default=True, description="Force real-time fetch")

class RoutedRequest(BaseModel):
    """Output of Workflow A (Router)."""
    original_query: str
    target_product_name: str
    target_url: str
    intent: str
    is_clarification_needed: bool = False
    clarification_question: Optional[str] = None
    force_refresh: bool = True
    
    @field_validator('target_url')
    def validate_url_official(cls, v):
        # Initial primitive check, real allow-list check happens in Scraper logic
        if "groww.in" not in v and "hdfcfund.com" not in v:
             raise ValueError("URL must be from an official domain (groww.in/hdfc)")
        return v

class KnowledgePacket(BaseModel):
    """Output of Workflow B (Knowledge)."""
    source_url: str
    content_markdown: str
    last_checked: datetime = Field(default_factory=datetime.utcnow)
    content_hash: str # SHA256 of the markdown content

    @field_validator('content_hash')
    def validate_hash(cls, v):
        if len(v) != 64: # SHA256 length
             raise ValueError("Invalid hash format")
        return v

class FeeExplanationBullet(BaseModel):
    """A single bullet point in the explanation."""
    text: str
    citation_url: str

class ValidatedResponse(BaseModel):
    """Output of Workflow C (Brain)."""
    answer_text: str
    bullets: List[FeeExplanationBullet]
    last_checked_str: str  # "Last checked: YYYY-MM-DD"
    sources_used: List[str]
    suggested_actions: List[Literal["EMAIL_SUPPORT", "SAVE_NOTES"]]
    prompt_version: str # e.g., "v1.2-beta"
    disclaimer_text: str = "This information is for educational purposes only and does not constitute investment advice."

class AuditLogEntry(BaseModel):
    """Immutable Audit Log."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    actor: str
    action_type: str
    action_payload: str # stringified JSON
    content_hash_snapshot: str  # What version of data was this based on?
    prompt_version_snapshot: str # What prompt produced this?
    
class MCPActionRequest(BaseModel):
    """Input for Node 4 (MCP)."""
    action: Literal["SAVE_NOTES", "EMAIL_SUPPORT"]
    payload: dict
    approval_token: str # Signed JWT or UUID from user session
    idempotency_key: str # UUID for dedup
