from pydantic import BaseModel, Field

class BuilderSummary(BaseModel):
    summary: str = Field(description="A 2-3 line summary of the provided information.")

class EvaluationResult(BaseModel):
    reasoning: str = Field(description="Reasoning for the evaluation.")
    score: float = Field(description="Score between 0.0 and 100.0 based on alignment.")

class FinalEvaluationResult(BaseModel):
    final_score: float = Field(description="The final weighted average score.")
    why_match: str = Field(description="A personalized paragraph explaining why the student and supervisor are a good match.")
