from typing import TypedDict


class CustomerFeedbackAnalysisState(TypedDict):
    input_text: str
    sentiment: str
    rectification_suggestion: str
    explanation: str
    action: str
    issue_type : str
