## Current Approach
<!-- For Self Reference -->

### Mapping of Student Profile to Supervisor Profile
Open Position <=> Research Interest + Summarized Intro Text + Raw Summary
Research Focus <=> Research Interest + Summarized Intro Text + Raw Summary
Evidence Papers + Grants <=> Skills, Projects + Education History

### Builder
Build following:
1. Summarized Intro Text + Raw Summary + Research Interest - 2, 3 Lines
2. Skills, Projects + Education History - 2, 3 Lines
3. Evidence Papers + Grants - 2, 3 Lines

### Evaluator
1. Evaluate each mapping mentioned above.
   - 0.45 for Open Position comparison
   - 0.35 for Research Focus comparison
   - 0.20 for Evidence comparison
   - reasoning for each evaluation

Open Position comparison - how well does the student's profile match the supervisor's open position?
Research Focus comparison - how well does the student's profile match the supervisor's research focus?
Evidence comparison - how well does the student's experience and skills match the supervisor's evidence papers and grants?

#### v0:
All comparisons run in parallel and score is calculated

#### v1:
Open Position comparison and Research Focus comparsion first run in parallel. If any of the score is less then 0.5, then the entry get rejected immediately. If both scores are above 0.5, then the Evidence comparison is run and final score is calculated.

Evidence score - only give confidence of getting selected based on student past skills and experience.

#### v2:
Supervisors fetched through "OpenAlex API". "NIH Grants API" is used to fetch active grants in case of US based supervisors. Countries standardization using `pycountry` library.

`Assumption:` Open Positions extraction was difficult, so assuming that Supervisors with recent active grants or recent papers are likely to have open positions in same field.

Data Quality Challenge solved:
1. Same-name-different-person collisions:
   - Topics ID is fetched first based on student profile's interests.
   - Only Authors mapped to a specific `topic_id` are considered as potential supervisors.
   - Recent 3 Topics and 5 Papers are fetched for each Author, so even if Author with irrelevant profile is fetched, they will be filtered out by the LLM in the Evaluator stage.

2. Final Score Calculation
    - Weighted average of the three evaluations > Final Score
    - Final reasoning based on the scores and individual evaluations - why_match

### DTO
1. For Builder:
- for Summarized Intro Text + Raw Summary + Research Interest - 2, 3 Lines - single key
- for Skills, Projects + Education History - 2, 3 Lines - single key
- for Evidence Papers + Grants - 2, 3 Lines - single key

2. For Evaluator:
- for Open Position comparison - keys: "reasoning", "score"
- for Research Focus comparison - keys: "reasoning", "score"
- for Evidence comparison - keys: "reasoning", "score"
- for Final Score Calculation - keys: "final_score", "why_match"

## Architecture
- Langchain chains
- HuggingFace Chat Models - Meta Llama 8B
