# PhD Shortlist Builder

## Context
PhD Shortlist — a personalised list of supervisors, programs, and funded opportunities surfaced for each
student, used downstream to draft personalised cold-emails to professors.
For each student, we need to produce a shortlist of ~50–200 actionable supervisor + program matches
that a domain mentor would unhesitatingly approve as worth contacting.

The challenge is not the LLM call. The challenge is the data: surfacing the right humans, with the right
evidence, in the right context, with no embarrassing mismatches.

## Goal
Build a system that ingests a student profile and produces a ranked shortlist of PhD supervisors +
programs, each with grant/paper evidence and a personalised why_match that a student can reference
when emailing the professor.

## Input
A student profile JSON containing:
```json
{
    "education_history": [
    {
        "degree": "BSc Computer Science",
        "institution": "University of Example",
        "grade": "First Class",
        "thesis": "Deep Learning for Natural Language Processing"
    }
    ],
    "skills": ["Python", "Machine Learning", "Data Analysis"],
    "projects": ["Sentiment Analysis of Social Media", "Image Classification with CNNs"],
    "publications": ["Smith, J. (2023). A Novel Approach to Machine Learning. Journal of AI Research."],
    "research_interests": ["Natural Language Processing", "Computer Vision", "Reinforcement Learning"],
    "target_countries": ["USA", "UK", "Canada"],
    "target_intake": "Fall 2025",
    "intro_call_summary": "The student is passionate about applying machine learning to real-world problems and
    has experience with both NLP and computer vision projects. They are particularly interested in working with supervisors who have a strong track record of industry collaboration.",
    "raw_resume_text": "John Smith is a recent graduate with a BSc in Computer Science from the University of Example. He graduated with First Class honors and completed a thesis on Deep Learning for Natural Language Processing. John has strong skills in Python, Machine Learning, and Data Analysis, and has worked on projects such as Sentiment Analysis of Social Media and Image Classification with CNNs. He has also published a paper titled 'A Novel Approach to Machine Learning' in the Journal of AI Research. John is targeting PhD programs in the USA, UK, and Canada for Fall 2025, and is particularly interested in supervisors with a strong track record of industry collaboration."
}
```

## Output
For each student, produce a single JSON shortlist:
50–200 supervisor recommendations

```json
{
    "student_id": "12345",
    "shortlist": [
        {
            "name": "Dr. Jane Doe",
            "institution": "University of Example",
            "country": "USA",
            "contact_email": "jane_doe@gmail.com",
            "research_focus": "Natural Language Processing and Industry Collaboration",
            "evidence": {
                "papers": [
                    "Doe, J. (2022). Industry Collaboration in NLP Research. Journal of AI Research."
                ],
                "grants": [
                    {
                        "title": "NLP for Real-World Applications",
                        "funder": "National Science Foundation",
                        "amount": "$500,000",
                        "link": "https://www.nsf.gov/grants/123456"
                    }
                ]
            },
            "why_match": "Dr. Doe's research on industry collaboration in NLP aligns perfectly with John's interest in applying machine learning to real-world problems. Her recent paper and NSF grant demonstrate her active engagement in this area.",
            "tier": "target", // (reach / target / safety)
            "linked_programs": [
                {
                    "program_name": "PhD in Computer Science",
                    "open_positions": [
                        {
                            "position_title": "PhD Research Assistant",
                            "application_deadline": "2024-12-01",
                            "link": "https://www.universityofexample.edu/phd_positions/12345"
                        }
                    ]
                }
            ]
        }
        // ... more supervisor entries ...
    ]
}
```

## Requirement
1. Coverage — ≥50 actionable recommendations spread across the student's stated areas
2. Country adherence — 100% within target countries (hard constraint)
3. Evidence — every supervisor must carry verifiable paper(s) or grant(s) with links
4. Personalisation — why_match must reference specific PI work that maps onto the student's profile, not
generic praise
5. Machine-readable output — consistent JSON schema, documented in the README
6. Reproducibility — given the same input, the system should run end-to-end with a single command
7. Latency — target wall-clock < 15 minutes per shortlist on a single laptop / one cloud VM

## Data Quality Challenges to Consider
### Same-name-different-person collisions
"Yang Shi", "Yu Meng", "Ying Ma", "Wei Wang", "Rong Zheng", "Sharma" are extremely common. The
supervisor you surface may be confused with an unrelated researcher of the same name. Catching the
mistake from a paper title alone is not enough — you need to verify the human matches the student's
research area before trusting them.

### Career-stage errors
PhD students and fresh postdocs appear in author databases with their own first-author papers, but they
cannot supervise PhDs. If you treat any name in an author list as a "PI", you will surface 24-year-old grad
students. Personal-award fellowships (NIH F31/F32, UKRI studentships, MSCA postdoc grants) list the
awardee — usually a junior researcher, not the supervisor.

### Wrong-domain leakage from keyword overlap
A grant titled "biodegradable plastic cartridges" can leak into a biomaterials student's list — it is
actually military ammunition R&D.
A grant on "high-elevation social-ecological systems" can leak into a Himalayan pilgrimage student's
list — it is actually Pacific Northwest fire archaeology.
A "trauma-informed" grant can leak into a clinical psychology student's list — it is actually a literaryhistory project on grief in Roman antiquity.
A "DNA barcoding" grant can leak into a plant biology student's list — it is actually single-cell
barcoding for human Hi-C chromatin work.
How do you tell discipline (humanities vs STEM vs medical) and region (which country / continent /
ecosystem) from a grant abstract before deciding it matches a student?

### Eligibility filters in free-text ads
Many PhD vacancies have citizenship/residency restrictions ("UK only", "home fees", "EU residents")
buried in the ad. Surfacing an ineligible position to an Indian student is worse than not surfacing it.
Consider how you would extract eligibility from unstructured ad text.
