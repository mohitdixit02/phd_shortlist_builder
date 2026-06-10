from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import json
import random
from service.data_provider import MockSupervisorProvider
from service.filters import apply_all_filters
from workflow.main import run_shortlist_pipeline

def main():
    # 1. Load students
    with open('mock_students.json', 'r') as f:
        students = json.load(f)
    
    if not students:
        print("No students found in mock_students.json.")
        return

    sample_student = random.choice(students)
    print(f"--- Processing Shortlist for: {sample_student['name']} ---")
    print(f"Target Countries: {sample_student['target_countries']}")
    
    # 2. Initialize the data provider
    from service.data_provider import APISupervisorProvider
    provider = APISupervisorProvider()
    all_supervisors = provider.fetch_supervisors(sample_student)
    print(f"Total supervisors fetched: {len(all_supervisors)}")
    
    # 3. Apply filters
    filtered_supervisors = apply_all_filters(all_supervisors, sample_student)
    print(f"Supervisors after filtering: {len(filtered_supervisors)}")
    
    if not filtered_supervisors:
        print("No supervisors matched the criteria.")
        return

    print("\nRunning LLM Pipeline...")
    shortlist = run_shortlist_pipeline(sample_student, filtered_supervisors)
    
    print("\n--- Final Personalized Shortlist ---")
    print(json.dumps(shortlist, indent=4))

if __name__ == "__main__":
    main()
