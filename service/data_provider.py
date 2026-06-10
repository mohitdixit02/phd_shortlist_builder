from abc import ABC, abstractmethod
import json
import os

class SupervisorProvider(ABC):
    """
    Abstract base class for supervisor data providers.
    This ensures that the rest of the system is independent of the data source.
    """
    @abstractmethod
    def fetch_supervisors(self) -> list[dict]:
        pass

class MockSupervisorProvider(SupervisorProvider):
    """
    Data provider that fetches supervisor information from a local mock JSON file.
    """
    def __init__(self, file_path: str = 'mock_supervisors.json'):
        self.file_path = file_path

    def fetch_supervisors(self) -> list[dict]:
        if not os.path.exists(self.file_path):
            print(f"Warning: {self.file_path} not found.")
            return []
        
        with open(self.file_path, 'r') as f:
            return json.load(f)
