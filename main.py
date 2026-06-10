import json
from service.data_provider import MockSupervisorProvider
from service.filters import apply_all_filters

def main():
    # 1. Find a student that has a target country available in our supervisor pool
    with open('mock_students.json', 'r') as f:
        students = json.load(f)
    
    with open('mock_supervisors.json', 'r') as f:
        all_sups = json.load(f)
    available_countries = set(s['country'].lower() for s in all_sups)
    
    sample_student = None
    for s in students:
        if any(c.lower() in available_countries for c in s['target_countries']):
            sample_student = s
            break
    
    if not sample_student:
        print("No student found with target countries in the supervisor pool.")
        return

    print(f"Processing student: {sample_student['name']}")
    print(f"Target Countries: {sample_student['target_countries']}")
    
    # 2. Initialize the data provider
    # This can be swapped with a real API provider later
    provider = MockSupervisorProvider('mock_supervisors.json')
    all_supervisors = provider.fetch_supervisors()
    print(f"Total supervisors fetched: {len(all_supervisors)}")
    
    # 3. Apply filters
    filtered_supervisors = apply_all_filters(all_supervisors, sample_student)
    
    print(f"Supervisors after filtering: {len(filtered_supervisors)}")
    
    # 4. Display a few results
    if filtered_supervisors:
        print("\nSample Filtered Supervisors:")
        for s in filtered_supervisors[:3]:
            print(f"- {s['name']} ({s['country']}) | Evidence: {len(s['evidence'].get('papers', []))} papers, {len(s['evidence'].get('grants', []))} grants")
    else:
        print("No supervisors matched the criteria.")

if __name__ == "__main__":
    main()
