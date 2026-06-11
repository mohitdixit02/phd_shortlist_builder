import pycountry

def get_strict_country_code(country_name: str) -> str:
    """
    Helper to strictly resolve country names to ISO codes.
    Raises ValueError on failure.
    """
    manual_map = {
        "UK": "GB",
        "UNITED KINGDOM": "GB",
        "USA": "US",
        "UNITED STATES": "US",
        "SOUTH KOREA": "KR",
        "VIETNAM": "VN"
    }
    name_upper = country_name.upper()
    if name_upper in manual_map:
        return manual_map[name_upper]

    try:
        return pycountry.countries.lookup(country_name).alpha_2
    except:
        raise ValueError(f"CRITICAL ERROR: Could not resolve country name '{country_name}' from student profile. Execution stopped.")

def filter_by_country(supervisors: list[dict], target_countries: list[str]) -> list[dict]:
    """
    Filter supervisors based on the student's target countries.
    Strictly validates target countries against ISO codes.
    """
    if not target_countries:
        return supervisors
    
    target_codes = [get_strict_country_code(c).upper() for c in target_countries]

    filtered_list = []
    for s in supervisors:
        sup_country = s.get('country', '').upper()
        if sup_country in target_codes:
            filtered_list.append(s)
                
    return filtered_list

def filter_by_evidence(supervisors: list[dict]) -> list[dict]:
    """
    Filter supervisors who do not have at least one paper or grant WITH a valid link.
    """
    filtered_list = []
    for s in supervisors:
        evidence = s.get('evidence', {})
        papers = evidence.get('papers', [])
        grants = evidence.get('grants', [])
        
        valid_papers = [p for p in papers if p.get('link') and str(p.get('link')).strip().lower() != 'n/a']
        valid_grants = [g for g in grants if g.get('link') and str(g.get('link')).strip().lower() != 'n/a']
        
        if len(valid_papers) > 0 or len(valid_grants) > 0:
            filtered_list.append(s)
            
    return filtered_list

def filter_by_openings(supervisors: list[dict]) -> list[dict]:
    """
    Filter supervisors who have potential openings.
    In the API version, any supervisor with linked programs or active grants is considered to have potential openings.
    """
    filtered_list = []
    for s in supervisors:
        programs = s.get('linked_programs', [])
        if programs:
            filtered_list.append(s)
            
    return filtered_list

def apply_all_filters(supervisors: list[dict], student_profile: dict) -> list[dict]:
    """
    Apply country, evidence, and openings filters sequentially with logging.
    """
    target_countries = student_profile.get('target_countries', [])
    
    print(f"LOG: Initial supervisors count: {len(supervisors)}")
    
    # Filter - Country
    filtered = filter_by_country(supervisors, target_countries)
    print(f"LOG: After COUNTRY filter: {len(filtered)} supervisors remain.")
    
    # Filter - Evidence
    filtered = filter_by_evidence(filtered)
    print(f"LOG: After EVIDENCE filter: {len(filtered)} supervisors remain.")
    
    # Filter - Open Positions
    filtered = filter_by_openings(filtered)
    print(f"LOG: After OPENINGS filter: {len(filtered)} supervisors remain.")
    
    return filtered
