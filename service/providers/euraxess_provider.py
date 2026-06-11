import requests
import xml.etree.ElementTree as ET
import pycountry
from service.providers.base import BaseSupervisorProvider

class EuraxessProvider(BaseSupervisorProvider):
    """
    Fetches real PhD vacancies across Europe via the Euraxess RSS feed.
    """
    RSS_URL = "https://euraxess.ec.europa.eu/job-feed"

    def fetch(self, student_profile: dict) -> list[dict]:
        interests = [i.lower() for i in student_profile.get("research_interests", [])]
        raw_targets = student_profile.get("target_countries", [])
        
        # Convert target countries to ISO codes for internal consistency
        target_isos = []
        for c in raw_targets:
            try:
                alias_map = {"UK": "GB", "USA": "US"}
                if c.upper() in alias_map:
                    target_isos.append(alias_map[c.upper()])
                else:
                    target_isos.append(pycountry.countries.lookup(c).alpha_2.upper())
            except:
                target_isos.append(c.upper())

        print(f"Fetching live Euraxess feed and filtering for {interests}...")
        
        try:
            response = requests.get(self.RSS_URL, timeout=10)
            if response.status_code != 200:
                print(f"Euraxess feed returned status {response.status_code}")
                return []
                
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            
            supervisors = []
            for item in items:
                title_elem = item.find("title")
                desc_elem = item.find("description")
                link_elem = item.find("link")
                creator_elem = item.find("{http://purl.org/dc/elements/1.1/}creator")
                
                title = title_elem.text if title_elem is not None else ""
                description = desc_elem.text if desc_elem is not None else ""
                link = link_elem.text if link_elem is not None else ""
                institution = creator_elem.text if creator_elem is not None else "Unknown Institution"
                
                title_desc = (title + " " + description).lower()
                if not any(interest in title_desc for interest in interests):
                    continue
                
                print(f"LOG: Euraxess Match found: {title}")
                
                country_code = "Unknown"
                for c_iso in target_isos:
                    try:
                        c_obj = pycountry.countries.get(alpha_2=c_iso)
                        possible_names = [c_obj.name.lower(), c_obj.alpha_2.lower()]
                        if hasattr(c_obj, 'common_name'): possible_names.append(c_obj.common_name.lower())
                        if hasattr(c_obj, 'official_name'): possible_names.append(c_obj.official_name.lower())
                        
                        if any(name in title_desc.lower() or name in institution.lower() for name in possible_names):
                            country_code = c_iso
                            break
                    except:
                        if c_iso.lower() in title_desc.lower() or c_iso.lower() in institution.lower():
                            country_code = c_iso
                            break
                
                # Special cases/Common European institution patterns
                if country_code == "Unknown":
                    common_map = {"PT": ["PORTUGAL", "LISBOA", "PORTO", "COIMBRA"], 
                                  "ES": ["SPAIN", "ESPAÑA", "BURGOS", "MADRID", "BARCELONA"],
                                  "DE": ["GERMANY", "DEUTSCHLAND", "MUNICH", "BERLIN", "MUNCHEN"],
                                  "FR": ["FRANCE", "PARIS", "LYON"],
                                  "NL": ["NETHERLANDS", "AMSTERDAM", "UTRECHT"]}
                    for iso, keywords in common_map.items():
                        if iso in target_isos:
                            if any(k.lower() in title_desc.lower() or k.lower() in institution.lower() for k in keywords):
                                country_code = iso
                                break
                
                programs = [{
                    "program_name": "PhD Program",
                    "open_positions": [{
                        "position_title": title,
                        "application_deadline": "Check Link",
                        "link": link
                    }]
                }]
                
                evidence_link = {"title": f"Job Posting: {title}", "link": link}
                
                supervisors.append(self._get_standard_supervisor(
                    name=f"Lead PI at {institution}",
                    institution=institution,
                    country=country_code,
                    focus=title,
                    papers=[evidence_link],
                    grants=[],
                    programs=programs
                ))
                
                if len(supervisors) >= 150: break
                
            return supervisors
            
        except Exception as e:
            print(f"Error fetching/parsing Euraxess feed: {e}")
            return []
