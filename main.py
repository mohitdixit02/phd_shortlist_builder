from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import json
import datetime
from service.data_provider import APISupervisorProvider
from service.filters import apply_all_filters
from workflow.main import run_shortlist_pipeline

def main():
    try:
        with open('input.json', 'r') as f:
            students = json.load(f)
    except FileNotFoundError:
        print("Error: input.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode input.json.")
        return
    
    if not students:
        print("No students found in input.json.")
        return

    all_results = {}
    provider = APISupervisorProvider()

    for student in students:
        name = student.get('name', 'Unknown Student')
        print(f"\n--- Processing Shortlist for: {name} ---")
        print(f"Target Countries: {student.get('target_countries', [])}")
        print(f"Research Interests: {student.get('research_interests', [])}")
        
        # 2. Fetch supervisors
        all_supervisors = provider.fetch_supervisors(student)
        print(f"Total supervisors fetched: {len(all_supervisors)}")
        
        filtered_supervisors = apply_all_filters(all_supervisors, student)
        print(f"Supervisors after filtering: {len(filtered_supervisors)}")
        
        if not filtered_supervisors:
            print(f"No supervisors matched the criteria for {name}.")
            all_results[name] = []
            continue

        print("Running LLM Pipeline...")
        shortlist = run_shortlist_pipeline(student, filtered_supervisors)
        all_results[name] = shortlist
        
        print(f"Shortlist for {name} generated with {len(shortlist)} candidates.")

    # 4. Write output to output_{date_time}.json
    date_time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"output_{date_time_str}.json"
    
    with open(output_filename, 'w') as f:
        json.dump(all_results, f, indent=4)
    
    print(f"\n--- Final Results saved to {output_filename} ---")

if __name__ == "__main__":
    main()
