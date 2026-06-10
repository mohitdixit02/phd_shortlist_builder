import json
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from models.builder import Builder
from models.evaluator import Evaluator

def run_shortlist_pipeline(student_profile, supervisors):
    """
    Orchestrates the builder and evaluator. LLMs are handled internally by models.
    """
    builder = Builder()
    evaluator = Evaluator()

    student_intent = builder.build_student_intent(
        student_profile.get("intro_call_summary", ""),
        student_profile.get("raw_resume_text", ""),
        student_profile.get("research_interests", [])
    )
    
    student_bg = builder.build_student_background(
        student_profile.get("skills", []),
        student_profile.get("projects", []),
        student_profile.get("education_history", [])
    )

    results = []

    for supervisor in supervisors:
        sup_evidence = builder.build_supervisor_evidence(
            supervisor.get("evidence", {}).get("papers", []),
            supervisor.get("evidence", {}).get("grants", [])
        )
        
        open_pos_text = ""
        if supervisor.get("linked_programs"):
            prog = supervisor["linked_programs"][0]
            if prog.get("open_positions"):
                open_pos_text = prog["open_positions"][0].get("position_title", "")

        eval_results = evaluator.evaluate_parallel({
            "position": {
                "open_position": open_pos_text,
                "student_intent": student_intent
            },
            "focus": {
                "research_focus": supervisor.get("research_focus", ""),
                "student_intent": student_intent
            },
            "evidence": {
                "supervisor_evidence": sup_evidence,
                "student_background": student_bg
            }
        })

        # Weighted Score Calculation
        pos_score = eval_results["position"].score
        focus_score = eval_results["focus"].score
        evid_score = eval_results["evidence"].score
        
        final_score = (pos_score * 0.45) + (focus_score * 0.35) + (evid_score * 0.20)

        # Final Reasoning (why_match)
        final_personalization = evaluator.generate_personalization(
            final_score,
            eval_results["position"].reasoning,
            eval_results["focus"].reasoning,
            eval_results["evidence"].reasoning
        )

        results.append({
            "name": supervisor["name"],
            "institution": supervisor["institution"],
            "final_score": final_score,
            "why_match": final_personalization.why_match,
            "details": {
                "position": {"score": pos_score, "reasoning": eval_results["position"].reasoning},
                "focus": {"score": focus_score, "reasoning": eval_results["focus"].reasoning},
                "evidence": {"score": evid_score, "reasoning": eval_results["evidence"].reasoning}
            }
        })

    # Sort results by score
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results
