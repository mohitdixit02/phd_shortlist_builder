from abc import ABC, abstractmethod

class BaseSupervisorProvider(ABC):
    """
    Abstract base class for regional supervisor discovery providers.
    Every provider must return a list of supervisor dictionaries in a standard format.
    """
    
    @abstractmethod
    def fetch(self, student_profile: dict) -> list[dict]:
        """
        Fetch supervisors based on the student's profile.
        Returns:
            list[dict]: A list of supervisors with name, institution, country, 
                        research_focus, evidence (with links), and linked_programs.
        """
        pass

    def _get_standard_supervisor(self, name, institution, country, focus, papers, grants, programs, is_pi=True):
        """
        Helper to ensure all providers return the same data structure.
        """
        return {
            "name": name,
            "institution": institution,
            "country": country,
            "contact_email": "N/A",
            "research_focus": focus,
            "evidence": {
                "papers": papers,
                "grants": grants
            },
            "is_pi": is_pi,
            "linked_programs": programs
        }
