import json
import random

def generate_mock_supervisors(count=50):
    first_names = ["Jane", "Michael", "Wei", "Sarah", "Ahmed", "Elena", "Takashi", "Maria", "David", "Linda", "Robert", "Susan", "James", "Karen", "Christopher", "Yang", "Yu", "Ying", "Wei", "Rong"]
    last_names = ["Doe", "Smith", "Wang", "Johnson", "Hassan", "Popescu", "Tanaka", "Garcia", "Brown", "Wilson", "Miller", "Davis", "Shi", "Meng", "Ma", "Wang", "Zheng"]
    
    institutions = [
        {"name": "University of Example", "country": "USA"},
        {"name": "Oxford University", "country": "UK"},
        {"name": "University of Toronto", "country": "Canada"},
        {"name": "ETH Zurich", "country": "Switzerland"},
        {"name": "Tsinghua University", "country": "China"},
        {"name": "University of Melbourne", "country": "Australia"},
        {"name": "Max Planck Institute", "country": "Germany"},
        {"name": "National University of Singapore", "country": "Singapore"}
    ]

    research_areas = [
        "Natural Language Processing", "Quantum Computing", "Marine Biology", 
        "Plant Genetics", "Clinical Psychology", "Bioinformatics", "Robotics", 
        "Reinforcement Learning", "Computer Vision", "Sustainable Energy"
    ]

    supervisors = []

    # 1. Normal PIs
    for i in range(count - 10):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        inst = random.choice(institutions)
        area = random.choice(research_areas)
        
        supervisors.append({
            "name": f"Dr. {fn} {ln}",
            "institution": inst["name"],
            "country": inst["country"],
            "contact_email": f"{fn.lower()}.{ln.lower()}@{inst['name'].lower().replace(' ', '')}.edu",
            "research_focus": f"{area} and its applications in {random.choice(research_areas)}",
            "evidence": {
                "papers": [
                    f"{ln}, {fn[0]}. (2022). Advances in {area}. Journal of {area} Research.",
                    f"{ln}, {fn[0]}. (2021). Modeling {area} using Deep Learning. Nature Research."
                ],
                "grants": [
                    {
                        "title": f"Future of {area}",
                        "funder": "National Science Foundation",
                        "amount": f"${random.randint(100, 900)},000",
                        "link": f"https://grants.gov/{random.randint(10000, 99999)}"
                    }
                ]
            },
            "is_pi": True,
            "linked_programs": [
                {
                    "program_name": f"PhD in {area}",
                    "open_positions": [
                        {
                            "position_title": "PhD Research Assistant",
                            "application_deadline": "2024-12-01",
                            "link": f"https://{inst['name'].lower().replace(' ', '')}.edu/jobs/{random.randint(100, 999)}",
                            "eligibility": "Open to all nationalities"
                        }
                    ]
                }
            ]
        })

    # 2. Collision Case: Two "Yang Shi"s
    collision_name = "Yang Shi"
    supervisors.append({
        "name": f"Dr. {collision_name}",
        "institution": "University of Example",
        "country": "USA",
        "contact_email": "yang.shi@example.edu",
        "research_focus": "Natural Language Processing",
        "evidence": {
            "papers": ["Shi, Y. (2023). Large Language Models. AI Journal."],
            "grants": [{"title": "NLP Grants", "funder": "NSF", "amount": "$500k", "link": "http://nsf.gov/1"}]
        },
        "is_pi": True,
        "linked_programs": []
    })
    supervisors.append({
        "name": f"Dr. {collision_name}",
        "institution": "Tsinghua University",
        "country": "China",
        "contact_email": "y_shi@tsinghua.edu.cn",
        "research_focus": "Marine Biology",
        "evidence": {
            "papers": ["Shi, Y. (2022). Coral Reef Ecosystems. Marine Science."],
            "grants": [{"title": "Ocean Bio Grant", "funder": "CNSF", "amount": "¥2M", "link": "http://cnsf.cn/2"}]
        },
        "is_pi": True,
        "linked_programs": []
    })

    # 3. Career-stage error: Postdoc (not a PI)
    supervisors.append({
        "name": "Dr. Junior Researcher",
        "institution": "Oxford University",
        "country": "UK",
        "contact_email": "junior.r@ox.ac.uk",
        "research_focus": "Quantum Computing",
        "evidence": {
            "papers": ["Researcher, J. (2024). My First Postdoc Paper. Quantum Letters."],
            "grants": [] # No PI-level grants
        },
        "is_pi": False,
        "linked_programs": []
    })

    # 4. Domain Leakage: "DNA Barcoding" for Human vs Plant
    supervisors.append({
        "name": "Dr. Plant Expert",
        "institution": "University of Toronto",
        "country": "Canada",
        "research_focus": "Plant Genetics using DNA Barcoding",
        "is_pi": True,
        "evidence": {"papers": ["Expert, P. (2023). DNA Barcoding for Alpine Flora."], "grants": [{"title": "Botanical Survey"}]}
    })
    supervisors.append({
        "name": "Dr. Human Geneticist",
        "institution": "Max Planck",
        "country": "Germany",
        "research_focus": "Human Chromatin Barcoding (Hi-C)",
        "is_pi": True,
        "evidence": {"papers": ["Geneticist, H. (2023). DNA Barcoding in Human Hi-C Data."], "grants": [{"title": "Cancer Research"}]}
    })

    # 5. Eligibility Restriction Case
    supervisors.append({
        "name": "Dr. Restricted Funding",
        "institution": "University of Example",
        "country": "USA",
        "research_focus": "Robotics",
        "is_pi": True,
        "evidence": {"papers": [], "grants": []},
        "linked_programs": [
            {
                "program_name": "PhD Robotics",
                "open_positions": [
                    {
                        "position_title": "Research Assistant",
                        "eligibility": "US Citizens Only (ITAR restricted)"
                    }
                ]
            }
        ]
    })

    return supervisors

if __name__ == "__main__":
    supervisors = generate_mock_supervisors(60)
    with open('mock_supervisors.json', 'w') as f:
        json.dump(supervisors, f, indent=4)
    print(f"Generated {len(supervisors)} mock supervisor entries in mock_supervisors.json")
