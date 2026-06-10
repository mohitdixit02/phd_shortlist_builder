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
import os

class Evaluator:
    """
    Provides evaluation chains for matching and personalization.
    """
    def __init__(self):
        self.llm = get_llm()
            
        # Structure matching user preference: prompt.partial(...) | model | parser
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

        # Encapsulated parallel chain
        self.parallel_eval_chain = RunnableParallel({
            "position": (lambda x: x["position"]) | self.position_chain,
            "focus": (lambda x: x["focus"]) | self.focus_chain,
            "evidence": (lambda x: x["evidence"]) | self.evidence_chain
        })

    def evaluate_parallel(self, inputs: dict) -> dict:
        """
        Runs the evaluation chains in parallel.
        """
        return self.parallel_eval_chain.invoke(inputs)

    def generate_personalization(self, final_score: float, pos_reasoning: str, focus_reasoning: str, evid_reasoning: str) -> dict:
        """
        Generates the final why_match statement.
        """
        return self.why_match_chain.invoke({
            "final_score": final_score,
            "position_reasoning": pos_reasoning,
            "focus_reasoning": focus_reasoning,
            "evidence_reasoning": evid_reasoning
        })
