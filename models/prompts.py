from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models.dto import BuilderSummary, EvaluationResult, FinalEvaluationResult

# Output Parsers
summary_parser = PydanticOutputParser(pydantic_object=BuilderSummary)
eval_parser = PydanticOutputParser(pydantic_object=EvaluationResult)
final_eval_parser = PydanticOutputParser(pydantic_object=FinalEvaluationResult)

SYSTEM_INSTRUCTIONS = """
<system>
You are a data extraction engine. You MUST output ONLY a valid JSON object.
Do NOT include any Python code, preamble, or conversational text.
</system>
"""

# Builder Prompts
BUILD_STUDENT_INTENT_PROMPT = PromptTemplate(
    template=SYSTEM_INSTRUCTIONS + """
    Summarize the student's research intent in 2-3 lines.
    
    CRITICAL: The 'Research Interest' field represents the student's PRIMARY CURRENT GOAL for their PhD. 
    You MUST prioritize the 'Research Interest' when defining the intent. 
    Use the 'Intro Text' and 'Raw Summary' ONLY to provide context on their motivation or how their background supports this interest, 
    but do NOT let them override the specific 'Research Interest' provided.
    
    Research Interest: {research_interest}
    Intro Text: {intro_text}
    Raw Summary: {raw_summary}
    
    {format_instructions}
    """,
    input_variables=["intro_text", "raw_summary", "research_interest"],
)

BUILD_STUDENT_BG_PROMPT = PromptTemplate(
    template=SYSTEM_INSTRUCTIONS + """
    Summarize the student's background in 2-3 lines based on their skills, projects, and education history. 
    Focus on relevant strengths for PhD research. 
    This summary will be used to evaluate technical fit with the supervisor's research evidence.
    Ensure skills, projects, and education are correctly captured.
    
    Skills: {skills}\nProjects: {projects}\nEducation: {education}
    
    {format_instructions}
    """,
    input_variables=["skills", "projects", "education"],
)

BUILD_SUPERVISOR_EVIDENCE_PROMPT = PromptTemplate(
    template=SYSTEM_INSTRUCTIONS + """
    Summarize the supervisor's research track record and evidence in 2-3 lines based on their recent papers and active grants.
    This evidence will be used to evaluate the technical alignment with the student's background.
    
    Papers: {papers}\nGrants: {grants}
    
    {format_instructions}
    """,
    input_variables=["papers", "grants"],
)

# Evaluator Prompts
EVALUATE_POSITION_PROMPT = PromptTemplate(
    template=SYSTEM_INSTRUCTIONS + """
    Evaluate the alignment between a specific supervisor's open PhD position and a student's research intent.
    
    CRITICAL: You must provide a numeric 'score' (0.0-100.0) and a separate 'reasoning' string.
    Do NOT put the score inside the reasoning text.
    
    Open Position: {open_position}\nStudent Intent: {student_intent}
    
    {format_instructions}
    """,
    input_variables=["open_position", "student_intent"],
)

EVALUATE_FOCUS_PROMPT = PromptTemplate(
    template=SYSTEM_INSTRUCTIONS + """
    Evaluate the alignment between the supervisor's overall research focus and the student's research intent.
    
    CRITICAL: You must provide a numeric 'score' (0.0-100.0) and a separate 'reasoning' string.
    Do NOT put the score inside the reasoning text.
    
    Research Focus: {research_focus}\nStudent Intent: {student_intent}
    
    {format_instructions}
    """,
    input_variables=["research_focus", "student_intent"],
)

EVALUATE_EVIDENCE_PROMPT = PromptTemplate(
    template=SYSTEM_INSTRUCTIONS + """
    Evaluate the technical alignment between the supervisor's publication/grant evidence and the student's skills/background.
    
    CRITICAL: You must provide a numeric 'score' (0.0-100.0) and a separate 'reasoning' string.
    Do NOT put the score inside the reasoning text.
    
    Supervisor Evidence: {supervisor_evidence}\nStudent Background: {student_background}
    
    {format_instructions}
    """,
    input_variables=["supervisor_evidence", "student_background"],
)

GENERATE_WHY_MATCH_PROMPT = PromptTemplate(
    template=SYSTEM_INSTRUCTIONS + """
    Generate a highly personalized 'why_match' statement (3-4 sentences) for the student's PhD shortlist. 
    
    CRITICAL: You MUST reference specific work from the 'Supervisor Evidence' (e.g., a specific paper topic, title, or grant) and explain exactly how it maps onto the student's background or PhD goals.
    Avoid generic praise like "This PI is a top target" or "Great alignment" without specific technical justification.
    
    Student Intent: {student_intent}
    Student Background: {student_background}
    Supervisor Evidence: {supervisor_evidence}
    Final Score: {final_score}
    
    {format_instructions}
    """,
    input_variables=["student_intent", "student_background", "supervisor_evidence", "final_score"],
)
