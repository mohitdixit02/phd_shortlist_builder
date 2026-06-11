# Output Schema Documentation

The system produces a JSON object where each key is a student's name, mapping to a list of personalized supervisor recommendations.

## Supervisor Object Schema

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | string | Full name of the supervisor/PI. |
| `institution` | string | University or Research Center. |
| `country` | string | ISO Country Code (e.g., GB, US). |
| `contact_email` | string | PI email address (defaults to "N/A" if unavailable). |
| `research_focus` | string | Primary research topics derived from publications/grants. |
| `evidence` | object | Contains lists of `papers` and `grants`. |
| `evidence.papers` | array | List of objects with `title` and `link` (DOI/URL). |
| `evidence.grants` | array | List of objects with `title`, `funder`, and `link`. |
| `final_score` | float | Weighted alignment score (0-100). |
| `tier` | string | Reach (>=85), Target (70-84), or Safety (<70). |
| `why_match` | string | Personalized blurb citing specific PI work and mapping it to the student. |
| `linked_programs` | array | List of PhD programs or specific open positions with links. |
| `details` | object | Internal scoring breakdown for Position, Focus, and Evidence. |

## Example Entry

```json
{
    "name": "Arkaitz Zubiaga",
    "institution": "Queen Mary University of London",
    "country": "GB",
    "contact_email": "a.zubiaga@qmul.ac.uk",
    "research_focus": "Natural Language Processing, Social Media Analysis",
    "evidence": {
        "papers": [
            {
                "title": "Synergizing machine learning & symbolic methods for NLP",
                "link": "https://doi.org/10.1145/1234567"
            }
        ],
        "grants": [
            {
                "title": "Project supported by UKRI - Misinformation Detection",
                "funder": "UKRI",
                "link": "https://gtr.ukri.org/projects?ref=EP/V0001"
            }
        ]
    },
    "final_score": 88.5,
    "tier": "Reach",
    "why_match": "The PI's recent work on 'Synergizing machine learning & symbolic methods' maps directly to your background in TensorFlow and interest in hybrid NLP models. Their work in misinformation detection provides a perfect technical framework for your PhD goals...",
    "linked_programs": [
        {
            "program_name": "PhD in Computer Science",
            "open_positions": [
                {
                    "position_title": "PhD Student in NLP & Misinformation",
                    "link": "https://www.qmul.ac.uk/postgraduate/research/subjects/computer-science/"
                }
            ]
        }
    ],
    "details": {
        "position": {
            "score": 90,
            "reasoning": "The open position on misinformation matches the student's intent perfectly."
        },
        "focus": {
            "score": 85,
            "reasoning": "High alignment between PI's NLP focus and student interests."
        },
        "evidence": {
            "score": 92,
            "reasoning": "PI's recent papers use exactly the tech stack mentioned in the student's resume."
        }
    }
}
```
