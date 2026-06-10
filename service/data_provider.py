from abc import ABC, abstractmethod
import requests
import pycountry
import os
import json
import time

IS_PI_THRESHOLD = int(os.getenv("IS_PI_THRESHOLD", 10))

class SupervisorProvider(ABC):
    """
    Abstract base class for supervisor data providers.
    This ensures that the rest of the system is independent of the data source.
    """
    @abstractmethod
    def fetch_supervisors(self, student_profile: dict) -> list[dict]:
        pass

class APISupervisorProvider(SupervisorProvider):
    """
    Data provider that fetches real-time researcher data from OpenAlex and NIH RePORTER.
    """
    OPENALEX_BASE_URL = "https://api.openalex.org"
    NIH_REPORTER_BASE_URL = "https://api.reporter.nih.gov/v2/projects/search"

    def __init__(self, email: str = "mohit.vsht@gmail.com"):
        self.email = email

    def _get_country_code(self, country_name: str) -> str:
        manual_map = {
            "UK": "GB",
            "UNITED KINGDOM": "GB",
            "USA": "US",
            "UNITED STATES": "US",
            "SOUTH KOREA": "KR",
            "VIETNAM": "VN"
        }
        name_upper = country_name.upper()
        if name_upper in manual_map:
            return manual_map[name_upper]

        try:
            return pycountry.countries.lookup(country_name).alpha_2
        except:
            raise ValueError(f"CRITICAL ERROR: Could not resolve country name '{country_name}' to an ISO code. Pipeline stopped!")

    def _get_topic_ids(self, interests: list[str]) -> list[str]:
        topic_ids = []
        for interest in interests:
            url = f"{self.OPENALEX_BASE_URL}/topics?search={interest}&mailto={self.email}"
            response = requests.get(url).json()
            if response.get("results"):
                full_id = response["results"][0]["id"]
                topic_ids.append(full_id.split("/")[-1])
        return list(set(topic_ids))

    def _fetch_authors(self, topic_ids: list[str], country_codes: list[str]) -> list[dict]:
        authors = []
        if not topic_ids or not country_codes:
            return authors

        topic_ids_str = "|".join(topic_ids)
        country_codes_str = "|".join(country_codes)
        
        filter_str = f"topics.id:{topic_ids_str},last_known_institutions.country_code:{country_codes_str}"
        url = f"{self.OPENALEX_BASE_URL}/authors?filter={filter_str}&per_page=200&sort=works_count:desc&mailto={self.email}"
        
        try:
            response = requests.get(url).json()
            return response.get("results", [])
        except:
            return []

    def _enrich_author_data(self, author: dict) -> dict:
        # Fetch recent works to get papers and potential grant info
        author_id = author["id"].split("/")[-1]
        works_url = f"{self.OPENALEX_BASE_URL}/works?filter=author.id:{author_id}&sort=publication_year:desc&per_page=5&mailto={self.email}"
        works_response = requests.get(works_url).json()
        works = works_response.get("results", [])

        papers = [w["title"] for w in works if w.get("title")]
        
        # Extract grants from works if available
        grants = []
        for work in works:
            for grant in work.get("grants", []):
                grants.append({
                    "title": f"Grant for: {work['title']}",
                    "funder": grant.get("funder_display_name", "Unknown"),
                    "amount": "Contact for details",
                    "link": work.get("doi", "N/A")
                })

        # NIH RePORTER check for US authors
        if author.get("last_known_institutions"):
            inst = author["last_known_institutions"][0]
            if inst.get("country_code") == "US":
                name_parts = author["display_name"].split()
                if len(name_parts) >= 2:
                    nih_grants = self._fetch_nih_grants(name_parts[0], name_parts[-1])
                    grants.extend(nih_grants)

        # Use active grants OR recent papers as a proxy for open positions
        linked_programs = []
        
        position_title = None
        position_link = author["id"]

        if grants:
            position_title = f"PhD Research Position - Project: {grants[0]['title']}"
            position_link = grants[0].get("link", author["id"])
        elif papers:
            position_title = f"PhD Research Position - Area: {papers[0]}"
        
        if position_title:
            linked_programs = [
                {
                    "program_name": "PhD Program",
                    "open_positions": [
                        {
                            "position_title": position_title,
                            "application_deadline": "See Institution Website",
                            "link": position_link
                        }
                    ]
                }
            ]

        return {
            "name": author["display_name"],
            "institution": author.get("last_known_institutions", [{}])[0].get("display_name", "Unknown"),
            "country": author.get("last_known_institutions", [{}])[0].get("country_code", "Unknown"),
            "contact_email": f"N/A (Check {author['id']})",
            "research_focus": ", ".join([t["display_name"] for t in author.get("topics", [])[:3]]),
            "evidence": {
                "papers": papers,
                "grants": grants
            },
            "is_pi": author.get("works_count", 0) > IS_PI_THRESHOLD,
            "linked_programs": linked_programs
        }

    def _fetch_nih_grants(self, first_name: str, last_name: str) -> list[dict]:
        payload = {
            "criteria": {
                "pi_names": [{"first_name": first_name, "last_name": last_name}]
            },
            "limit": 3
        }
        try:
            response = requests.post(self.NIH_REPORTER_BASE_URL, json=payload).json()
            nih_grants = []
            for proj in response.get("results", []):
                nih_grants.append({
                    "title": proj.get("project_title"),
                    "funder": "NIH",
                    "amount": f"${proj.get('total_amount', 'N/A')}",
                    "link": f"https://reporter.nih.gov/project-details/{proj.get('appl_id')}"
                })
            return nih_grants
        except:
            return []

    def fetch_supervisors(self, student_profile: dict) -> list[dict]:
        interests = student_profile.get("research_interests", [])
        target_countries = student_profile.get("target_countries", [])
        
        country_codes = [self._get_country_code(c) for c in target_countries]
        country_codes = [c for c in country_codes if c]

        print(f"Mapping topics for: {interests}...")
        topic_ids = self._get_topic_ids(interests)
        
        print(f"Fetching authors for topics {topic_ids} in {country_codes}...")
        authors = self._fetch_authors(topic_ids, country_codes)
        
        print(f"Enriching data for {len(authors[:150])} candidates...")
        supervisors = []
        for i, author in enumerate(authors[:150]):
            if (i + 1) % 10 == 0:
                print(f"Enriched {i + 1}/{len(authors[:150])}...")
            supervisors.append(self._enrich_author_data(author))
            time.sleep(0.05) # Faster delay for higher volume
            
        return supervisors

class MockSupervisorProvider(SupervisorProvider):
    """
    Data provider that fetches supervisor information from a local mock JSON file.
    """
    def __init__(self, file_path: str = 'mock_supervisors.json'):
        self.file_path = file_path

    def fetch_supervisors(self, student_profile: dict = None) -> list[dict]:
        if not os.path.exists(self.file_path):
            print(f"Warning: {self.file_path} not found.")
            return []
        
        with open(self.file_path, 'r') as f:
            return json.load(f)
