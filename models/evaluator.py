from models.prompts import (
    EVALUATE_POSITION_PROMPT, 
    EVALUATE_FOCUS_PROMPT, 
    EVALUATE_EVIDENCE_PROMPT, 
    GENERATE_WHY_MATCH_PROMPT, 
    eval_parser, 
    final_eval_parser
)
from service.model_provider import get_llm
from langchain_core.runnables import RunnableParallel

class Evaluator:
    """
    Provides evaluation chains for matching and personalization.
    """
    def __init__(self):
        self.llm = get_llm()
            
        self.position_chain = (
            EVALUATE_POSITION_PROMPT.partial(format_instructions=eval_parser.get_format_instructions()) 
            | self.llm 
            | eval_parser
        )
        self.focus_chain = (
            EVALUATE_FOCUS_PROMPT.partial(format_instructions=eval_parser.get_format_instructions()) 
            | self.llm 
            | eval_parser
        )
        self.evidence_chain = (
            EVALUATE_EVIDENCE_PROMPT.partial(format_instructions=eval_parser.get_format_instructions()) 
            | self.llm 
            | eval_parser
        )
        self.why_match_chain = (
            GENERATE_WHY_MATCH_PROMPT.partial(format_instructions=final_eval_parser.get_format_instructions()) 
            | self.llm 
            | final_eval_parser
        )

        self.alignment_chain = RunnableParallel({
            "position": (lambda x: x["position"]) | self.position_chain,
            "focus": (lambda x: x["focus"]) | self.focus_chain
        })

    def evaluate_alignment(self, inputs: dict) -> dict:
        """
        Runs Position and Focus evaluations in parallel (v1 Step 1).
        """
        return self.alignment_chain.invoke(inputs)

    def evaluate_evidence(self, inputs: dict) -> dict:
        """
        Runs Evidence evaluation (v1 Step 2).
        """
        return self.evidence_chain.invoke(inputs)

    def generate_personalization(self, final_score: float, student_intent: str, student_bg: str, sup_evidence: str) -> dict:
        """
        Generates the final why_match statement.
        """
        return self.why_match_chain.invoke({
            "final_score": final_score,
            "student_intent": student_intent,
            "student_background": student_bg,
            "supervisor_evidence": sup_evidence
        })
