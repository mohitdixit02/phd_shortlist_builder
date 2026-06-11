import requests
import pycountry
import os
from service.providers.base import BaseSupervisorProvider

IS_PI_THRESHOLD = int(os.getenv("IS_PI_THRESHOLD", 10))

class OpenAlexProvider(BaseSupervisorProvider):
    """
    Fetches supervisors from OpenAlex using grant-funder filters for UK, CA, AU.
    Also serves as a general-purpose fallback for global discovery.
    """
    BASE_URL = "https://api.openalex.org"

    def __init__(self, email: str = "mohit.vsht@gmail.com"):
        self.email = email

    def _get_country_code(self, country_name: str) -> str:
        manual_map = {"UK": "GB", "USA": "US", "SOUTH KOREA": "KR"}
        name_upper = country_name.upper()
        if name_upper in manual_map: return manual_map[name_upper]
        try:
            return pycountry.countries.lookup(country_name).alpha_2
        except:
            return None

    def fetch(self, student_profile: dict) -> list[dict]:
        interests = student_profile.get("research_interests", [])
        target_countries = student_profile.get("target_countries", [])
        
        country_codes = [self._get_country_code(c) for c in target_countries]
        country_codes = [c for c in country_codes if c]
        
        if not country_codes: return []

        print(f"Searching OpenAlex (Grants) for {interests} in {country_codes}...")
        
        topic_ids = self._get_topic_ids(interests)
        if not topic_ids: return []

        funder_ids = self._get_funder_ids(country_codes)
        if not funder_ids:
            print("LOG: No major funders found for these countries.")
            return []

        topic_str = "|".join(topic_ids)
        funder_str = "|".join(funder_ids)
        
        filter_str = (
            f"topics.id:{topic_str},"
            f"funders.id:{funder_str},"
            f"publication_year:>2023"
        )
        url = f"{self.BASE_URL}/works?filter={filter_str}&per_page=200&sort=cited_by_count:desc&mailto={self.email}"
        
        try:
            response = requests.get(url).json()
            works = response.get("results", [])
            print(f"LOG: Found {len(works)} works with specific funder matches.")
            supervisors_map = {}
            
            for work in works:
                for author_entry in work.get("authorships", []):
                    author = author_entry.get("author")
                    if not author or not author.get("id"): continue
                    
                    author_id = author["id"].split("/")[-1]
                    
                    if author_id in supervisors_map: continue
                    
                    author_details = self._fetch_author_details(author_id)
                    if not author_details: continue
                    
                    enriched = self._enrich_author(author_details, work)
                    if enriched:
                        supervisors_map[author_id] = enriched
                        if len(supervisors_map) >= 300: break
                if len(supervisors_map) >= 300: break
            
            return list(supervisors_map.values())
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error in OpenAlex fetch: {e}")
            return []

    def _get_topic_ids(self, interests: list[str]) -> list[str]:
        ids = []
        for interest in interests:
            url = f"{self.BASE_URL}/topics?search={interest}&mailto={self.email}"
            res = requests.get(url).json()
            if res.get("results"):
                ids.append(res["results"][0]["id"].split("/")[-1])
        return list(set(ids))

    def _get_funder_ids(self, country_codes: list[str]) -> list[str]:
        """
        Fetch top 50 funders for the given country codes.
        """
        country_str = "|".join(country_codes)
        url = f"{self.BASE_URL}/funders?filter=country_code:{country_str}&sort=works_count:desc&per_page=50&mailto={self.email}"
        try:
            res = requests.get(url).json()
            ids = []
            for f in res.get("results", []):
                if f.get("id"):
                    ids.append(f["id"].split("/")[-1])
            return ids
        except:
            return []

    def _fetch_author_details(self, author_id: str) -> dict:
        url = f"{self.BASE_URL}/authors/{author_id}?mailto={self.email}"
        try:
            return requests.get(url).json()
        except:
            return None

    def _enrich_author(self, author: dict, primary_work: dict) -> dict:
        evidence_work = {
            "title": primary_work.get("title"),
            "link": primary_work.get("doi") or primary_work.get("id") or "N/A"
        }
        
        raw_funders = primary_work.get("grants", [])
        if not raw_funders:
            raw_funders = []
            for f in primary_work.get("funders", []):
                if f.get("display_name"):
                    raw_funders.append({"funder_display_name": f["display_name"], "funder": f.get("id", "Unknown")})

        if not raw_funders:
            return None 

        grants = []
        for g in raw_funders:
            grants.append({
                "title": f"Project supported by: {g.get('funder_display_name', 'Unknown Funder')}",
                "funder": g.get("funder_display_name", "Unknown"),
                "link": evidence_work["link"]
            })
            
        funder_name = grants[0]["funder"]
        programs = [{
            "program_name": "Funded PhD Research",
            "open_positions": [{
                "position_title": f"PhD Position - Funded by {funder_name} (Topic: {primary_work['title']})",
                "application_deadline": "Contact PI regarding funding",
                "link": evidence_work["link"]
            }]
        }]

        last_inst = author.get("last_known_institutions")
        institution = "Unknown"
        country_code = "Unknown"
        if last_inst and len(last_inst) > 0:
            institution = last_inst[0].get("display_name", "Unknown")
            country_code = last_inst[0].get("country_code", "Unknown")

        return self._get_standard_supervisor(
            name=author.get("display_name", "Unknown"),
            institution=institution,
            country=country_code,
            focus=", ".join([t["display_name"] for t in author.get("topics", [])[:3]]),
            papers=[evidence_work],
            grants=grants,
            programs=programs,
            is_pi=author.get("works_count", 0) > IS_PI_THRESHOLD
        )
