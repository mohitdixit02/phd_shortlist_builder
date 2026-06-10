from models.prompts import (
    BUILD_STUDENT_INTENT_PROMPT, 
    BUILD_STUDENT_BG_PROMPT, 
    BUILD_SUPERVISOR_EVIDENCE_PROMPT, 
    summary_parser
)
from service.model_provider import get_llm
import json
import os

class Builder:
    """
    Summarizes student and supervisor data.
    """
    def __init__(self):
        self.llm = get_llm()
        
        # Structure matching user preference: prompt.partial(...) | model | parser
        self.intent_chain = (
            BUILD_STUDENT_INTENT_PROMPT.partial(format_instructions=summary_parser.get_format_instructions()) 
            | self.llm 
            | summary_parser
        )
        self.bg_chain = (
            BUILD_STUDENT_BG_PROMPT.partial(format_instructions=summary_parser.get_format_instructions()) 
            | self.llm 
            | summary_parser
        )
        self.evidence_chain = (
            BUILD_SUPERVISOR_EVIDENCE_PROMPT.partial(format_instructions=summary_parser.get_format_instructions()) 
            | self.llm 
            | summary_parser
        )

    def build_student_intent(self, intro_text: str, raw_summary: str, research_interest: list) -> str:
        res = self.intent_chain.invoke({
            "intro_text": intro_text,
            "raw_summary": raw_summary,
            "research_interest": json.dumps(research_interest)
        })
        # res is a Pydantic object (BuilderSummary)
        return res.summary

    def build_student_background(self, skills: list, projects: list, education: list) -> str:
        res = self.bg_chain.invoke({
            "skills": json.dumps(skills),
            "projects": json.dumps(projects),
            "education": json.dumps(education)
        })
        return res.summary

    def build_supervisor_evidence(self, papers: list, grants: list) -> str:
        res = self.evidence_chain.invoke({
            "papers": json.dumps(papers),
            "grants": json.dumps(grants)
        })
        return res.summary
