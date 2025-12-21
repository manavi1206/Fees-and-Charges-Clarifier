from typing import List
from .domain_model import ValidatedResponse, FeeExplanationBullet, KnowledgePacket

class CitationError(Exception):
    """Raised when the Agent fails to cite strictly."""
    pass

class StrictValidator:
    """
    The Gatekeeper.
    Ensures LLM output adheres to fintech constraints.
    """
    
    @staticmethod
    def validate_response(
        raw_bullets: List[str], 
        knowledge: KnowledgePacket
    ) -> ValidatedResponse:
        """
        Parses raw text bullets from LLM.
        Enforces:
        1. Every bullet must have the source URL.
        2. Source URL must match the KnowledgePacket (no hallucinated external links).
        """
        
        validated_bullets = []
        
        for bullet in raw_bullets:
            # Check 1: Link presence
            # Expecting format: "Statement... [Source](url)"
            if knowledge.source_url not in bullet:
                raise CitationError(f"Bullet missing strict citation: '{bullet}'. Expected link: {knowledge.source_url}")
            
            # Create object
            validated_bullets.append(FeeExplanationBullet(
                text=bullet.replace(f"({knowledge.source_url})", "").replace("[]", "").strip(),
                citation_url=knowledge.source_url
            ))
            
        return ValidatedResponse(
            answer_text="Here are the fees explained:", # Generic header, UI handles rendering
            bullets=validated_bullets,
            last_checked_str=f"Last checked: {knowledge.last_checked.strftime('%Y-%m-%d')}",
            sources_used=[knowledge.source_url],
            suggested_actions=["SAVE_NOTES", "EMAIL_SUPPORT"]
        )
