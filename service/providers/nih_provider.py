import requests
from service.providers.base import BaseSupervisorProvider
import os
from datetime import datetime

IS_PI_THRESHOLD = int(os.getenv("IS_PI_THRESHOLD", 10))

class NIHProvider(BaseSupervisorProvider):
    """
    Fetches high-confidence open positions in the USA via NIH RePORTER grants.
    """
    NIH_REPORTER_BASE_URL = "https://api.reporter.nih.gov/v2/projects/search"

    def fetch(self, student_profile: dict) -> list[dict]:
        interests = student_profile.get("research_interests", [])
        target_countries = [c.upper() for c in student_profile.get("target_countries", [])]
        
        if "USA" not in target_countries and "UNITED STATES" not in target_countries and "US" not in target_countries:
            return []

        print(f"Searching NIH RePORTER for: {interests}...")
        
        current_year = datetime.now().year
        years = [current_year, current_year - 1, current_year - 2]
        
        payload = {
            "criteria": {
                "keywords": interests,
                "project_nums": ["R01", "R21", "T32", "P01"], # Focus on active research grants
                "fiscal_years": years # Look at recent years
            },
            "limit": 300,
            "sort_field": "fiscal_year",
            "sort_order": "desc"
        }
        
        try:
            response = requests.post(self.NIH_REPORTER_BASE_URL, json=payload).json()
            results = response.get("results", [])
            supervisors = []
            
            for proj in results:
                pi_name = proj.get("contact_pi_name", "Unknown")
                if pi_name == "Unknown": continue
                
                parts = pi_name.split(",")
                if len(parts) == 2:
                    formatted_name = f"{parts[1].strip()} {parts[0].strip()}"
                else:
                    formatted_name = pi_name

                grant_title = proj.get("project_title")
                grant_link = f"https://reporter.nih.gov/project-details/{proj.get('appl_id')}"
                
                grant_info = {
                    "title": grant_title,
                    "funder": "NIH",
                    "amount": f"${proj.get('total_amount', 'N/A')}",
                    "link": grant_link
                }

                programs = [
                    {
                        "program_name": "PhD Program",
                        "open_positions": [
                            {
                                "position_title": f"PhD Research Position - Project: {grant_title}",
                                "application_deadline": "Contact PI / See Institution Website",
                                "link": grant_link
                            }
                        ]
                    }
                ]

                supervisors.append(self._get_standard_supervisor(
                    name=formatted_name,
                    institution=proj.get("organization", {}).get("org_name", "Unknown"),
                    country="US",
                    focus=grant_title, # Focus derived from grant
                    papers=[], # RePORTER doesn't easily give recent papers in one go
                    grants=[grant_info],
                    programs=programs
                ))
            
            return supervisors
        except Exception as e:
            print(f"Error fetching from NIH: {e}")
            return []
