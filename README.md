# CareerMate - Multi-Agent Career Advisor

👋 Welcome to **CareerMate**, an intelligent multi-agent system designed to assist users in exploring and planning their career paths. It uses specialized AI agents to analyze skill gaps, find relevant jobs, and recommend learning resources.

---

## 🎯 Project Objective

CareerMate helps users by:

- Identifying missing skills for a desired career goal based on current skill sets.
- Suggesting job opportunities aligned with user skills and preferences.
- Recommending online courses tailored to bridge the user's skill gaps.

---

## 🤖 System Overview

### Agents

- **Conversation Agent (CareerMate Main Controller)**  
  Handles user interactions, detects intent, and routes queries to appropriate specialist agents for detailed assistance.

- **Skill Gap Agent**  
  Compares user's current skills against target job requirements and identifies missing skills.  
  Uses the tool: `get_missing_skills(current_skills, career_goal)`.

- **Job Finder Agent**  
  Searches job listings based on career goals and optionally location.  
  Uses the tool: `find_jobs(career_goal, location)`.

- **Course Recommender Agent**  
  Suggests relevant courses to learn missing skills.  
  Uses the tool: `recommend_courses(missing_skills)`.

---

## 🛠️ Implemented Tools

- **get_missing_skills:** Returns missing and suggested skills for a target career goal using dummy skill mappings.
- **find_jobs:** Provides job listings with title, company, location, salary, and relevance based on user career goals.
- **recommend_courses:** Recommends online courses based on missing skills, including platform, duration, difficulty, and topics.

---

## 🛠️ How it responds-
<img width="1534" height="788" alt="Screenshot 2025-08-01 175250" src="https://github.com/user-attachments/assets/8d7b8b64-0561-43ce-a6b8-82f7cccbe6b2" />
<img width="1505" height="559" alt="Screenshot 2025-08-01 175353" src="https://github.com/user-attachments/assets/8723a33d-2dff-4626-bcf9-ebc0159b0007" />



