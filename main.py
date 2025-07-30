import os
import json
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import  Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled


# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL") 
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME") 

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set BASE_URL, API_KEY, and MODEL_NAME."
    )


client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)
    
# --- Models for structured outputs ---
    
class SkillGap(BaseModel):
    career_goal: str
    current_skills: List[str]
    missing_skills: List[str]
    suggested_skills_to_learn: List[str]
    skill_gap_reasoning: str = Field(description="Why these skills are essential for the target career")

class JobFinder(BaseModel):
    job_title: str
    company: str
    location: str
    salary_range: Optional[str] = Field(default=None, description="Optional salary range if available")
    job_description: str
    application_link: str
    relevance_reason: str = Field(description="Why this job matches the user's profile or goal")

class CourseRecommender(BaseModel):
    course_title: str
    platform: str
    duration_weeks: int
    difficulty_level: str  # e.g., Beginner, Intermediate, Advanced
    link: str
    topics_covered: List[str]
    recommendation_reason: str
    
# --- Tools ---

@function_tool
def get_missing_skills(current_skills: List[str], career_goal: str) -> str:
    """Identify missing skills based on current skills and desired career goal."""
    # Dummy data for skill requirements
    required_skills = {
    "Data Scientist": ["Python", "Pandas", "SQL", "Machine Learning", "Data Visualization", "Deep Learning"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Git"],
    "AI Engineer": ["Python", "TensorFlow", "PyTorch", "ML Algorithms", "Data Structures", "MLOps"],
    "Mobile App Developer": ["Java", "Kotlin", "Swift", "Flutter", "React Native", "Firebase"],
    "DevOps Engineer": ["Linux", "Docker", "Kubernetes", "CI/CD", "AWS", "Terraform"],
    "Cybersecurity Analyst": ["Network Security", "Python", "Ethical Hacking", "Penetration Testing", "SIEM", "Firewalls"],
    "Data Analyst": ["Excel", "SQL", "Tableau", "Power BI", "Python", "Statistics"],
    "UI/UX Designer": ["Figma", "Adobe XD", "Sketch", "User Research", "Wireframing", "Prototyping"],
    "Cloud Engineer": ["AWS", "Azure", "Google Cloud", "Linux", "Python", "Terraform"],
    "Machine Learning Engineer": ["Python", "Scikit-learn", "TensorFlow", "Data Preprocessing", "Model Evaluation", "MLOps"],
    "Backend Developer": ["Node.js", "Django", "Flask", "REST APIs", "MongoDB", "PostgreSQL"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Vue.js", "Webpack"]
}


    missing_skills = []
    suggestions = []

    if career_goal in required_skills:
        goal_skills = set(required_skills[career_goal])
        current = set(current_skills)
        missing_skills = list(goal_skills - current)
        suggestions = missing_skills[:3]  # Just show top 3 to focus

    result = {
        "career_goal": career_goal,
        "current_skills": current_skills,
        "missing_skills": missing_skills,
        "suggested_skills_to_learn": suggestions,
        "skill_gap_reasoning": f"These skills are commonly required in {career_goal} job listings and are essential for competence in the role."
    }

    return json.dumps(result)


@function_tool
def find_jobs(career_goal: str, location: Optional[str] = "Remote") -> str:
    """Find job listings based on the career goal and location."""
    jobs = [
    {
        "job_title": "Junior Data Scientist",
        "company": "InsightTech",
        "location": location,
        "salary_range": "$60,000 - $75,000",
        "job_description": "Analyze data, build ML models, and generate business insights.",
        "application_link": "https://jobs.insighttech.com/junior-ds",
        "relevance_reason": "Entry-level position suitable for aspiring data scientists with foundational skills."
    },
    {
        "job_title": "ML Engineer Intern",
        "company": "AI Next",
        "location": location,
        "salary_range": "Paid Internship",
        "job_description": "Work on deploying ML models and data pipelines.",
        "application_link": "https://ainext.com/careers/ml-intern",
        "relevance_reason": "Excellent opportunity to gain hands-on experience in a practical ML role."
    },
    {
        "job_title": "Frontend Web Developer",
        "company": "BrightCode",
        "location": location,
        "salary_range": "$50,000 - $65,000",
        "job_description": "Develop responsive and dynamic web interfaces using React and JavaScript.",
        "application_link": "https://brightcode.dev/jobs/frontend",
        "relevance_reason": "Ideal for developers with strong HTML, CSS, and React skills."
    },
    {
        "job_title": "Backend Node.js Developer",
        "company": "CodeBase Inc.",
        "location": location,
        "salary_range": "$65,000 - $80,000",
        "job_description": "Develop APIs and handle server-side logic using Node.js and Express.",
        "application_link": "https://codebase.io/careers/backend-node",
        "relevance_reason": "Good fit for candidates with server-side development experience using Node.js."
    },
    {
        "job_title": "AI Engineer - Computer Vision",
        "company": "VisionAI",
        "location": location,
        "salary_range": "$85,000 - $110,000",
        "job_description": "Design and implement deep learning models for image classification and object detection.",
        "application_link": "https://visionai.jobs/ai-computer-vision",
        "relevance_reason": "Great role for engineers skilled in PyTorch and TensorFlow."
    },
    {
        "job_title": "MLOps Engineer",
        "company": "PipelineTech",
        "location": location,
        "salary_range": "$90,000 - $120,000",
        "job_description": "Build CI/CD pipelines and deploy ML models at scale.",
        "application_link": "https://pipelinetech.io/jobs/mlops",
        "relevance_reason": "Excellent for those with experience in ML workflows and DevOps practices."
    },
    {
        "job_title": "Full Stack Web Developer",
        "company": "DevLoop",
        "location": location,
        "salary_range": "$70,000 - $90,000",
        "job_description": "Work on both frontend and backend technologies to build scalable web applications.",
        "application_link": "https://devloop.io/jobs/fullstack",
        "relevance_reason": "Requires proficiency in JavaScript, React, Node.js, and Git."
    }
]


    return json.dumps(jobs)


@function_tool
def recommend_courses(missing_skills: List[str]) -> str:
    """Recommend online courses based on missing skills."""
    course_catalog = {
    "Python": {
        "course_title": "Python for Everybody",
        "platform": "Coursera",
        "duration_weeks": 8,
        "difficulty_level": "Beginner",
        "link": "https://coursera.org/python-for-everybody",
        "topics_covered": ["Python basics", "Data structures", "Web access"],
        "recommendation_reason": "Best for beginners starting Python."
    },
    "Machine Learning": {
        "course_title": "Machine Learning by Andrew Ng",
        "platform": "Coursera",
        "duration_weeks": 11,
        "difficulty_level": "Intermediate",
        "link": "https://coursera.org/learn/machine-learning",
        "topics_covered": ["Supervised learning", "Unsupervised learning", "Model evaluation"],
        "recommendation_reason": "Highly recommended foundational ML course."
    },
    "React": {
        "course_title": "React - The Complete Guide",
        "platform": "Udemy",
        "duration_weeks": 6,
        "difficulty_level": "Intermediate",
        "link": "https://udemy.com/react-complete-guide",
        "topics_covered": ["Components", "State management", "Hooks"],
        "recommendation_reason": "Covers practical React development from scratch."
    },
    "Docker": {
        "course_title": "Docker Mastery: with Kubernetes +Swarm",
        "platform": "Udemy",
        "duration_weeks": 5,
        "difficulty_level": "Intermediate",
        "link": "https://udemy.com/course/docker-mastery",
        "topics_covered": ["Docker basics", "Container orchestration", "Kubernetes", "Swarm mode"],
        "recommendation_reason": "Essential course for mastering containerization and orchestration."
    },
    "Deep Learning": {
        "course_title": "Deep Learning Specialization",
        "platform": "Coursera",
        "duration_weeks": 16,
        "difficulty_level": "Advanced",
        "link": "https://coursera.org/specializations/deep-learning",
        "topics_covered": ["Neural Networks", "CNNs", "RNNs", "Sequence Models"],
        "recommendation_reason": "Comprehensive specialization by Andrew Ng for deep learning enthusiasts."
    },
    "AWS Fundamentals": {
        "course_title": "AWS Fundamentals: Going Cloud-Native",
        "platform": "Coursera",
        "duration_weeks": 4,
        "difficulty_level": "Beginner",
        "link": "https://coursera.org/learn/aws-fundamentals-going-cloud-native",
        "topics_covered": ["Cloud concepts", "AWS core services", "Cloud-native architectures"],
        "recommendation_reason": "Ideal starting point for learning cloud computing with AWS."
    },
    "Cybersecurity": {
        "course_title": "Introduction to Cyber Security",
        "platform": "edX",
        "duration_weeks": 6,
        "difficulty_level": "Beginner",
        "link": "https://edx.org/course/introduction-to-cyber-security",
        "topics_covered": ["Security basics", "Threats and vulnerabilities", "Risk management"],
        "recommendation_reason": "Great course for those starting in cybersecurity."
    }
}


    recommended = [course_catalog[skill] for skill in missing_skills if skill in course_catalog]

    return json.dumps(recommended)

# --- Specialist Agents ---

skill_gap_agent = Agent(
    name="Skill Gap Specialist",
    handoff_description="Identifies missing skills based on user's current skills and career goal",
    instructions="""
    You are a Skill Gap Specialist who helps users understand what skills they need to learn to reach a particular career goal.
    
    Use the get_missing_skills tool to analyze the user's current skills and compare them to the target role.
    
    Clearly list the missing skills, suggest top skills to learn next, and explain why they are important.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[get_missing_skills],
    output_type=SkillGap
)

job_finder_agent = Agent(
    name="Job Finder",
    handoff_description="Finds jobs based on user's career goal and preferences",
    instructions="""
    You are a Job Finder Specialist who searches for job listings based on the user's career interests.
    
    Use the find_jobs tool to locate relevant job listings. Always explain why a job matches the user’s profile and how it aligns with their goals.
    
    Present job title, company, location, salary (if available), and a brief description.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[find_jobs],
    output_type=JobFinder
)

course_recommender_agent = Agent(
    name="Course Recommender",
    handoff_description="Recommends courses based on the user's missing or required skills",
    instructions="""
    You are a Course Recommender Specialist who helps users upskill by suggesting relevant online courses.
    
    Use the recommend_courses tool based on the user's missing skills. Present course name, platform, duration, and topics covered.
    
    Clearly explain why each course is a good fit for the user's learning path.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[recommend_courses],
    output_type=CourseRecommender
)

# --- Main Multi-Agent System ---

career_mate_agent = Agent(
    name="CareerMate",
    instructions="""
    You are CareerMate — a comprehensive multi-agent career advisor.

    You help users:
    1. Discover what skills they are missing to reach their career goal
    2. Find relevant jobs matching their goals
    3. Recommend the best courses to bridge skill gaps

    Use your specialist agents to handle specific queries related to skill analysis, job finding, and course recommendation.

    Always guide users step-by-step and hand off to the right specialist when needed.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    handoffs=[skill_gap_agent, job_finder_agent, course_recommender_agent]
)




async def main():
    print("👋 Hi! I'm CareerMate — your multi-agent career assistant.")
    print("You can ask me things like:")
    print(" - What skills do I need to become a data scientist?")
    print(" - Can you find me a remote ML job?")
    print(" - Suggest courses for deep learning.\n")
    print("Type 'exit' anytime to quit.\n")

    while True:
        user_query = input("🧑 You: ")
        if user_query.lower() in ["exit", "quit"]:
            print("👋 Goodbye! Wishing you success in your career journey.")
            break

        # Let CareerMate decide which agent to use based on its instructions
        result = await Runner.run(career_mate_agent, user_query)

        print("\n🤖 CareerMate's Response:")

        final = result.final_output

        # Display result depending on what type was returned
        if hasattr(final, "career_goal"):
            print("\n📉 SKILL GAP ANALYSIS 📉")
            print(f"Career Goal: {final.career_goal}")
            print("Current Skills:", ", ".join(final.current_skills))
            print("Missing Skills:", ", ".join(final.missing_skills))
            print("Top Skills to Learn:", ", ".join(final.suggested_skills_to_learn))
            print(f"\n📝 Reasoning: {final.skill_gap_reasoning}\n")

        elif hasattr(final, "job_title"):
            print("\n💼 JOB RECOMMENDATION 💼")
            print(f"Job Title: {final.job_title}")
            print(f"Company: {final.company}")
            print(f"Location: {final.location}")
            if final.salary_range:
                print(f"Salary: {final.salary_range}")
            print(f"Description: {final.job_description}")
            print(f"Apply here: {final.application_link}")
            print(f"\n🔍 Why this job: {final.relevance_reason}\n")

        elif hasattr(final, "course_title"):
            print("\n🎓 COURSE RECOMMENDATION 🎓")
            print(f"Course Title: {final.course_title}")
            print(f"Platform: {final.platform}")
            print(f"Duration: {final.duration_weeks} weeks")
            print(f"Difficulty Level: {final.difficulty_level}")
            print(f"Link: {final.link}")
            print("Topics Covered:")
            for i, topic in enumerate(final.topics_covered, 1):
                print(f"  {i}. {topic}")
            print(f"\n📌 Why this course: {final.recommendation_reason}\n")

        elif isinstance(final, list) and all(hasattr(c, "course_title") for c in final):
            print("\n🎓 MULTIPLE COURSE RECOMMENDATIONS 🎓")
            for i, course in enumerate(final, 1):
                print(f"\n📘 Course {i}: {course.course_title}")
                print(f"  Platform: {course.platform}")
                print(f"  Duration: {course.duration_weeks} weeks")
                print(f"  Difficulty: {course.difficulty_level}")
                print(f"  Link: {course.link}")
                print(f"  Topics: {', '.join(course.topics_covered)}")
                print(f"  Reason: {course.recommendation_reason}")
            print()

        else:
            print(final)


if __name__ == "__main__":
    asyncio.run(main())