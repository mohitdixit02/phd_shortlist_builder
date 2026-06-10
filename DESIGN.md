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
   - Run in parallel

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
