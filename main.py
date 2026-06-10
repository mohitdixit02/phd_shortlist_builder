import json
import random
from service.data_provider import MockSupervisorProvider
from service.filters import apply_all_filters
from workflow.main import run_shortlist_pipeline
from dotenv import load_dotenv

def main():
    load_dotenv()  # Load environment variables from .env file
    # 1. Find a random student that has a target country available in our supervisor pool
    with open('mock_students.json', 'r') as f:
        students = json.load(f)
    
    with open('mock_supervisors.json', 'r') as f:
        all_sups = json.load(f)
    available_countries = set(s['country'].lower() for s in all_sups)
    
    eligible_students = [s for s in students if any(c.lower() in available_countries for c in s['target_countries'])]
    
    if not eligible_students:
        print("No student found with target countries in the supervisor pool.")
        return

    sample_student = random.choice(eligible_students)
    print(f"--- Processing Shortlist for: {sample_student['name']} ---")
    print(f"Target Countries: {sample_student['target_countries']}")
    
    # 2. Initialize the data provider
    provider = MockSupervisorProvider('mock_supervisors.json')
    all_supervisors = provider.fetch_supervisors()
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
