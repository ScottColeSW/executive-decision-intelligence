"""
Executive Decision Intelligence
Decision Case Domain Model
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class DecisionCase:
    id: str
    title: str
    company: str
    question: str

    investment: float
    expected_return: float

    confidence: float = 0.0

    assumptions: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)

    recommendation: str = ""
    
    context: str = ""
    question: str