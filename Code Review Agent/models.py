from typing import List, Literal
from pydantic import BaseModel, Field

class ReviewItem(BaseModel):
    category: Literal["Security", "Performance", "Style", "Bug"]
    severity: Literal["High", "Medium", "Low"]
    line_number: int = Field(..., description="Approximate or exact line number of the issue")
    issue: str = Field(..., description="Concise description of the problem")
    recommendation: str = Field(..., description="Actionable fix or code snippet")

class CodeReviewReport(BaseModel):
    summary: str = Field(..., description="Overall assessment of the code quality")
    findings: List[ReviewItem] = Field(..., description="List of identified issues and vulnerabilities")
    refactored_code: str = Field(..., description="The fully cleaned, secure, and optimized version of the code")