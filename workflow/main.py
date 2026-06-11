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
        open_pos_text = ""
        if supervisor.get("linked_programs"):
            prog = supervisor["linked_programs"][0]
            if prog.get("open_positions"):
                open_pos_text = prog["open_positions"][0].get("position_title", "")

        # Initial Alignment (Position & Focus)
        alignment_results = evaluator.evaluate_alignment({
            "position": {
                "open_position": open_pos_text,
                "student_intent": student_intent
            },
            "focus": {
                "research_focus": supervisor.get("research_focus", ""),
                "student_intent": student_intent
            }
        })

        pos_score = alignment_results["position"].score
        focus_score = alignment_results["focus"].score

        if pos_score < 50 or focus_score < 50:
            # Candidate rejected, skip to next supervisor
            print(f"Supervisor {supervisor['name']} rejected due to low alignment scores (Position: {pos_score}, Focus: {focus_score}).")
            continue

        sup_evidence = builder.build_supervisor_evidence(
            supervisor.get("evidence", {}).get("papers", []),
            supervisor.get("evidence", {}).get("grants", [])
        )
        
        evid_results = evaluator.evaluate_evidence({
            "supervisor_evidence": sup_evidence,
            "student_background": student_bg
        })
        evid_score = evid_results.score
        
        # Weighted Score Calculation
        final_score = (pos_score * 0.45) + (focus_score * 0.35) + (evid_score * 0.20)

        # Final Reasoning (why_match)
        final_personalization = evaluator.generate_personalization(
            final_score,
            alignment_results["position"].reasoning,
            alignment_results["focus"].reasoning,
            evid_results.reasoning
        )

        # Calculate Tier
        tier = "Safety"
        if final_score >= 85:
            tier = "Reach"
        elif final_score >= 70:
            tier = "Target"

        results.append({
            "name": supervisor["name"],
            "institution": supervisor["institution"],
            "country": supervisor.get("country", "N/A"),
            "contact_email": supervisor.get("contact_email", "N/A"),
            "research_focus": supervisor.get("research_focus", "N/A"),
            "evidence": supervisor.get("evidence", {}),
            "final_score": final_score,
            "tier": tier,
            "why_match": final_personalization.why_match,
            "linked_programs": supervisor.get("linked_programs", []),
            "details": {
                "position": {"score": pos_score, "reasoning": alignment_results["position"].reasoning},
                "focus": {"score": focus_score, "reasoning": alignment_results["focus"].reasoning},
                "evidence": {"score": evid_score, "reasoning": evid_results.reasoning}
            }
        })

    # Sort results by score
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results
