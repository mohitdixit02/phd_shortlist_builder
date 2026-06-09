import json
import random

def generate_mock_students(count=22):
    names = [
        'John Smith', 'Maria Garcia', 'Lin Chen', 'Emma Johnson', 'Wei Wang', 
        'Sofia Rodriguez', 'Liam Brown', 'Yuki Tanaka', 'Amira Hassan', 'Lucas Mueller', 
        'Chloe Dubois', 'Aarav Patel', 'Isabella Conti', 'Dmitry Volkov', 'Zeynep Yilmaz', 
        'Kofi Mensah', 'Elena Popescu', 'Ji-won Kim', 'Mateo Fernandez', 'Anika Sharma', 
        'Gabriel Santos', 'Olivia Wilson'
    ]
    countries = ['USA', 'UK', 'Canada', 'Australia', 'New Zealand', 'Germany', 'France', 'Netherlands', 'Ireland']
    interests = [
        'Natural Language Processing', 'Computer Vision', 'Reinforcement Learning', 
        'Plant Genetics', 'Clinical Psychology', 'Bioinformatics', 'Robotics', 
        'Quantum Computing', 'Marine Biology', 'Public Health', 'Sustainable Energy', 
        'Human-Computer Interaction'
    ]
    skills_pool = [
        'Python', 'Machine Learning', 'Data Analysis', 'R', 'Bioinformatics', 
        'Qualitative Analysis', 'C++', 'TensorFlow', 'PyTorch', 'SQL', 'GIS', 'Lab Techniques'
    ]

    data = []
    for i in range(count):
        name = names[i % len(names)]
        student_id = f"stu_{100+i}"
        target_cnts = random.sample(countries, random.randint(1, 3))
        res_interests = random.sample(interests, random.randint(1, 3))
        skills = random.sample(skills_pool, random.randint(2, 5))
        
        profile = {
            "id": student_id,
            "name": name,
            "education_history": [
                {
                    "degree": f"BSc in {res_interests[0]}",
                    "institution": f"University of {name.split()[-1]}",
                    "grade": random.choice(['First Class', 'High Distinction', '3.9 GPA', '1.0 (German Scale)']),
                    "thesis": f"Advanced Research in {res_interests[0]}"
                }
            ],
            "skills": skills,
            "projects": [f"Project on {res_interests[0]}", f"Analysis of {random.choice(interests)}"],
            "publications": [f"{name.split()[-1]}, {name[0]}. (2023). Future of {res_interests[0]}. {random.choice(['Journal of Science', 'AI Review', 'Nature Research'])}."],
            "research_interests": res_interests,
            "target_countries": target_cnts,
            "target_intake": "Fall 2025",
            "intro_call_summary": f"{name} is highly motivated to pursue a PhD in {res_interests[0]}. They have experience in {skills[0]} and are looking for a supervisor who specializes in {res_interests[0]}.",
            "raw_resume_text": f"{name} graduated with honors from University of {name.split()[-1]}. Skills include {', '.join(skills)}. Interested in {', '.join(res_interests)}."
        }
        data.append(profile)
    
    return data

if __name__ == "__main__":
    students = generate_mock_students(25)
    with open('mock_students.json', 'w') as f:
        json.dump(students, f, indent=4)
    print(f"Generated {len(students)} mock student profiles in mock_students.json")
