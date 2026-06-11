from abc import ABC, abstractmethod
import os
import json
from service.providers.factory import ProviderFactory

class SupervisorProvider(ABC):
    """
    Abstract base class for supervisor data providers.
    """
    @abstractmethod
    def fetch_supervisors(self, student_profile: dict) -> list[dict]:
        pass

class APISupervisorProvider(SupervisorProvider):
    """
    Orchestrator that dispatches to regional providers (NIH, Euraxess, OpenAlex).
    """
    def fetch_supervisors(self, student_profile: dict) -> list[dict]:
        target_countries = student_profile.get("target_countries", [])
        
        providers = ProviderFactory.get_providers(target_countries)
        
        all_supervisors = []
        for provider in providers:
            try:
                results = provider.fetch(student_profile)
                all_supervisors.extend(results)
            except Exception as e:
                print(f"Provider {provider.__class__.__name__} failed: {e}")
        
        print(f"Total high-confidence candidates found: {len(all_supervisors)}")
        return all_supervisors

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
