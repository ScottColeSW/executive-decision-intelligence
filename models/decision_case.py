from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class CaseType(str, Enum):
    CAPEX = "capex"
    SUNK_COST = "sunk_cost"
    AI_ROI = "ai_roi"

class FinancialMetrics(BaseModel):
    initial_investment: float = Field(..., description="Upfront capital required")
    projected_annual_return: Optional[float] = None
    sunk_costs_to_date: float = Field(default=0.0)
    time_horizon_years: int = Field(default=5)
    risk_adjusted_discount_rate: float = Field(default=0.10, description="WACC or hurdle rate")

class DecisionCase(BaseModel):
    case_id: str
    title: str
    case_type: CaseType
    description: str
    financials: FinancialMetrics
    assumptions: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)