import pandas as pd
import random

# --- CONFIGURATION ---
NUM_STUDENTS = 5000       # Increased for better training
NUM_INTERNSHIPS = 1000    # Increased to provide more options

# --- 1. EXPANDED COMPANY DATABASE ---
# 50+ diverse company names to prevent model bias
companies = [
    'TechSol', 'DataMinds', 'InnovateX', 'CloudNet', 'SoftSystems', 'AlphaTech', 'CyberDyne',
    'BlueWave', 'OrbitTech', 'Nexus Solutions', 'PrimeLogic', 'CoreSystems', 'Vanguard Data',
    'Summit Digital', 'Apex Innovations', 'Quantum Bits', 'Fusion Labs', 'Starlight Systems',
    'Omega Corp', 'Horizon Tech', 'Pioneer Soft', 'Vertex Global', 'Infinity AI', 'RapidScale',
    'LogicGate', 'SparkNet', 'CodeCraft', 'ByteWorks', 'Visionary Apps', 'NextLevel Tech',
    'Titan Software', 'Aether Dynamics', 'Helios Data', 'Sierra Logic', 'Delta Force',
    'Echo Systems', 'Novus Tech', 'Zenith AI', 'Polaris Solutions', 'Meridian Soft',
    'Equinox Labs', 'Solstice Tech', 'TerraFirm', 'LunaSys', 'Stellar Code', 'Nebula Data',
    'Cosmos AI', 'Galactic Soft', 'Universal Tech', 'Global Connect', 'Future Systems',
    'Smart Solutions', 'Bright Ideas', 'ClearView Tech', 'DeepDive Data', 'FastTrack Soft'
]

locations = ['Remote', 'Bangalore', 'Hyderabad', 'Pune', 'Mumbai', 'Delhi', 'Chennai', 'Gurgaon', 'Noida', 'Indore']

# --- 2. ROLE-SKILL MAPPING (Kept for Accuracy) ---
role_skills_map = {
    'Data Scientist': ['Python', 'Machine Learning', 'Deep Learning', 'Data Science', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'SQL', 'Tableau'],
    'Data Analyst': ['Python', 'SQL', 'Excel', 'Tableau', 'Power BI', 'Data Science', 'Statistics', 'R'],
    'Software Engineer': ['Java', 'C++', 'Python', 'Data Structures', 'Algorithms', 'SQL', 'Git', 'System Design'],
    'Backend Developer': ['Java', 'Spring Boot', 'Node.js', 'Express.js', 'Django', 'Flask', 'SQL', 'NoSQL', 'MongoDB', 'PostgreSQL', 'API Design'],
    'Frontend Developer': ['JavaScript', 'React', 'Angular', 'Vue.js', 'HTML', 'CSS', 'Tailwind CSS', 'Redux', 'TypeScript'],
    'Full Stack Developer': ['JavaScript', 'React', 'Node.js', 'MongoDB', 'SQL', 'HTML', 'CSS', 'Express.js', 'Git'],
    'DevOps Engineer': ['AWS', 'Azure', 'Docker', 'Kubernetes', 'Linux', 'Jenkins', 'CI/CD', 'Git', 'Bash Scripting'],
    'Machine Learning Engineer': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'Deep Learning', 'MLOps', 'AWS', 'Docker'],
    'Product Manager': ['Agile', 'JIRA', 'Product Management', 'Data Analysis', 'SQL', 'Communication', 'Roadmapping'],
    'UI/UX Designer': ['Figma', 'Adobe XD', 'Sketch', 'HTML', 'CSS', 'Wireframing', 'Prototyping', 'User Research'],
    'Mobile App Developer': ['Java', 'Kotlin', 'Swift', 'Flutter', 'React Native', 'Android Studio', 'iOS Development'],
    'QA Engineer': ['Selenium', 'Java', 'Python', 'JIRA', 'Manual Testing', 'Automation Testing', 'SQL'],
    'System Administrator': ['Linux', 'Windows Server', 'Networking', 'Bash', 'AWS', 'Azure', 'Virtualization']
}
roles_pool = list(role_skills_map.keys())

# --- 3. GENERATE STUDENTS ---
students = []
for i in range(NUM_STUDENTS):
    preferred_role = random.choice(roles_pool)
    relevant_skills = role_skills_map[preferred_role]
    
    # Pick 3-6 skills relevant to the role
    num_skills = random.randint(3, min(6, len(relevant_skills)))
    student_skills_list = random.sample(relevant_skills, k=num_skills)
    
    # 10% chance to add a random extra skill (noise)
    all_skills_flat = [s for sub in role_skills_map.values() for s in sub]
    if random.random() < 0.1:
         student_skills_list.append(random.choice(all_skills_flat))

    # Academic stats for Placement Prediction
    cgpa = round(random.uniform(6.0, 9.9), 2)
    mock_score = random.randint(40, 99)
    projects = random.randint(0, 6)
    internships_done = random.randint(0, 3)
    
    # Weighted score for realistic placement status
    score = (cgpa * 10) + mock_score + (projects * 5) + (internships_done * 10)
    placed = 1 if score > 165 else 0  # Slightly stricter threshold
    
    students.append({
        "Student_ID": f"2025CS{10000+i}",
        "Name": f"Student_{i}",
        "Skills": ", ".join(list(set(student_skills_list))),
        "Preferred_Role": preferred_role,
        "CGPA": cgpa,
        "Mock_OA_Score": mock_score,
        "Projects": projects,
        "Internships_Done": internships_done,
        "Placed_Status": placed
    })

# --- 4. GENERATE INTERNSHIPS (With diverse companies) ---
internships = []
for i in range(NUM_INTERNSHIPS):
    role = random.choice(roles_pool)
    comp = random.choice(companies) # Pick from the large list
    loc = random.choice(locations)
    
    relevant_skills = role_skills_map[role]
    num_req = random.randint(3, min(5, len(relevant_skills)))
    req_skills = random.sample(relevant_skills, k=num_req)
    
    internships.append({
        "Internship_ID": f"INT_{5000+i}",
        "Company": comp,
        "Role": role,
        "Location": loc,
        "Stipend": random.choice([5000, 8000, 10000, 12000, 15000, 20000, 25000, 'Unpaid']),
        "Required_Skills": ", ".join(req_skills),
        "Description": f"Join {comp} as a {role}. We need expertise in {', '.join(req_skills[:2])}."
    })

# --- SAVE FILES ---
df_students = pd.DataFrame(students)
df_internships = pd.DataFrame(internships)

df_students.to_csv("comprehensive_students_data.csv", index=False)
df_internships.to_csv("comprehensive_company_data.csv", index=False)

print(f"Generated {NUM_STUDENTS} students and {NUM_INTERNSHIPS} internships across {len(companies)} companies.")