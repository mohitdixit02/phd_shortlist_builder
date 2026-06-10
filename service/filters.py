def filter_by_country(supervisors: list[dict], target_countries: list[str]) -> list[dict]:
    """
    Filter supervisors based on the student's target countries.
    """
    if not target_countries:
        return supervisors
    
    # Standardize to lowercase for comparison
    target_countries_lower = [c.lower() for c in target_countries]
    
    return [
        s for s in supervisors 
        if s.get('country', '').lower() in target_countries_lower
    ]

def filter_by_evidence(supervisors: list[dict]) -> list[dict]:
    """
    Filter supervisors who do not have at least one paper or grant.
    """
    filtered_list = []
    for s in supervisors:
        evidence = s.get('evidence', {})
        papers = evidence.get('papers', [])
        grants = evidence.get('grants', [])
        
        if len(papers) > 0 or len(grants) > 0:
            filtered_list.append(s)
            
    return filtered_list

def filter_by_openings(supervisors: list[dict]) -> list[dict]:
    """
    Filter supervisors who do not have at least one open position in their linked programs.
    """
    filtered_list = []
    for s in supervisors:
        programs = s.get('linked_programs', [])
        has_opening = False
        for prog in programs:
            if len(prog.get('open_positions', [])) > 0:
                has_opening = True
                break
        if has_opening:
            filtered_list.append(s)
            
    return filtered_list

def apply_all_filters(supervisors: list[dict], student_profile: dict) -> list[dict]:
    """
    Apply country, evidence, and openings filters sequentially.
    """
    target_countries = student_profile.get('target_countries', [])
    
    # Filter - Country
    filtered = filter_by_country(supervisors, target_countries)
    
    # Filter - Evidence
    filtered = filter_by_evidence(filtered)
    
    # Filter - Open Positions
    filtered = filter_by_openings(filtered)
    
    return filtered
