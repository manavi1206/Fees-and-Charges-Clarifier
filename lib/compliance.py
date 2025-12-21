from typing import Optional, Tuple, Dict, List
from .domain_model import RefusalReason

class FeeScenarioRegistry:
    """
    Registry of allowed fee scenarios and their required clarifications.
    Addition 3: Versioned Registry to handle drift.
    """
    VERSION = "1.1" # Bumped after adding TAXATION/TRANSACTION_LIMITS
    
    # Map of Intent -> List of Potential Clarifiers
    # The Brain will select which one is relevant based on context.
    SCENARIOS: Dict[str, List[str]] = {
        "EXIT_LOAD": ["Is this for SIP or Lumpsum?", "What is the holding period?"],
        "EXPENSE_RATIO": ["Direct or Regular plan?"],
        "STAMP_DUTY": [], # Usually flat, no clarifier needed
        "TAXATION": ["Short-term (<1yr) or Long-term (>1yr)?"],
        "TRANSACTION_LIMITS": ["SIP or Lumpsum investment?"],
        "SIP_CHARGES": [],
        "OIRC_CHARGES": [],
        "TRANSACTION_CHARGES": []
    }

    @classmethod
    def get_clarifiers(cls, intent: str) -> List[str]:
        return cls.SCENARIOS.get(intent, [])

class RefusalMatrix:
    """
    Deterministic Compliance Engine.
    Evaluates queries against strict refusal rules.
    """
    
    # Static rules for keyword matching (First line of defense)
    FORBIDDEN_KEYWORDS = {
        "COMPARISON": ["better than", "vs", "compare", "beat", "peer", "whiteoak", "edelweiss", "nippon"],
        "ADVICE": ["should i", "recommend", "is it good", "buy or sell", "rating", "very high risk"],
        "PERFORMANCE": ["returns", "cagr", "profit", "prediction", "forecast", "1-year", "3-year", "5-year", "all-time"],
        "HYPOTHETICAL": ["if i had", "what if", "scenario"],
        "OUT_OF_SCOPE": ["nav", "fund size", "net asset value", "aum"]
    }
    
    REGULATORY_MESSAGES = {
        "COMPARISON": "As a Fee Explainer Agent, I adhere to SEBI guidelines and cannot provide comparisons between different mutual fund schemes. Please consult a registered investment advisor.",
        "ADVICE": "I am an informational agent designed to explain fees and charges only. I cannot provide investment advice, ratings, or recommendations.",
        "PERFORMANCE": "I do not discuss historical performance or future predictions. My scope is strictly limited to the current Schedule of Fees available on official documents.",
        "HYPOTHETICAL": "I can only explain fees based on current factual data. I cannot simulate hypothetical investment scenarios beyond standard calculations.",
        "PII": "I cannot process personal identifiable information.",
        "OUT_OF_SCOPE": "I am specialized in Fees & Charges. General fund information like NAV, AUM, or Fund Managers is out of my scope.",
        "UNDOCUMENTED_FEE": "This specific fee is not mentioned in the official scheme documents. I cannot invent or infer fees."
    }

    @classmethod
    def check_compliance(cls, query: str) -> Optional[RefusalReason]:
        """
        Returns a RefusalReason if the query violates compliance.
        Returns None if the query is clean.
        """
        query_lower = query.lower()
        
        # 1. PII Check (Simple heuristic for demo)
        if any(x in query_lower for x in ["pan", "aadhar", "mobile", "password"]):
             return RefusalReason(
                reason_code="PII",
                regulatory_message=cls.REGULATORY_MESSAGES["PII"]
            )

        # 2. Keyword Refusals
        for category, keywords in cls.FORBIDDEN_KEYWORDS.items():
            if any(k in query_lower for k in keywords):
                return RefusalReason(
                    reason_code=category, # type: ignore
                    regulatory_message=cls.REGULATORY_MESSAGES[category]
                )
                
        return None
