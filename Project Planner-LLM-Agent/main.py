# Packages
import warnings
from helper import load_env
import os 
import yaml
from crewai import Agent, Task, Crew
from typing import List
from pydantic import BaseModel, Field
import pandas as pd



# Warning check
warnings.filterwarnings('ignore')

# Set environments
load_env()
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'

# Define file paths for YAML configurations
files = {
    'agents':'config/agents.yaml',
    'tasks': 'config/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']

# Create pydantic models for structured output
class TaskEstimate(BaseModel):
    task_name: str = Field(..., description='Name of the task')
    estimated_time_hours: float = Field(..., description='Estimated time to complete the task in hours')
    required_resources: List[str] = Field(..., description='List of resources required to complete the task')

class Milestone(BaseModel):
    milestone_name: str = Field(..., description='Name of the milestone')
    tasks: List[str] = Field(..., description='List of task IDs associated with this milestone')

class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = Field(..., description='List of tasks with their estimates')
    milestones: List[Milestone] = Field(..., description='List of project milestones')

# Creating agents 
project_planning_agent = Agent(config = agents_config['project_planning_agent'])
estimation_agent = Agent(config=agents_config['estimation_agent'])
resource_allocation_agent = Agent(config=agents_config['resource_allocation_agent'])

# Creating tasks
task_breakdown = Task(config=tasks_config['task_breakdown'], agent=project_planning_agent)
time_resource_estimation = Task(config=tasks_config['time_resource_estimation'], agent=estimation_agent)
resource_allocation = Task(config=tasks_config['resource_allocation'], agent=resource_allocation_agent, output_pydantic=ProjectPlan) 

# Creating crew
crew = Crew(agents=[project_planning_agent, estimation_agent, resource_allocation_agent], 
            tasks=[task_breakdown, time_resource_estimation, resource_allocation],
            verbose=True)

# Inputs
project = 'Website'
industry = 'Technology'
project_objectives = 'Create a website for a small business'
team_members = """
- John Doe (Project Manager)
- Jane Doe (Software Engineer)
- Bob Smith (Designer)
- Alice Johnson (QA Engineer)
- Tom Brown (QA Engineer)
"""

project_requirements = """
- Create a responsive design that works well on desktop and mobile devices
- Implement a modern, visually appealing user interface with a clean look
- Develop a user-friendly navigation system with intuitive menu structure
- Include an "About Us" page highlighting the company's history and values
- Design a "Services" page showcasing the business's offerings with descriptions
- Create a "Contact Us" page with a form and integrated map for communication
- Implement a blog section for sharing industry news and company updates
- Ensure fast loading times and optimize for search engines (SEO)
- Integrate social media links and sharing capabilities
- Include a testimonials section to showcase customer feedback and build trust
"""

# Format the dictionary as Markdown for a better display
formatted_output = f"""
**Project Type:** {project}

**Project Objectives:** {project_objectives}

**Industry:** {industry}

**Team Members:**
{team_members}
**Project Requirements**
{project_requirements}
"""
# Crew
inputs = {
    'project_type': project,
    'project_objectives': project_objectives,
    'industry': industry,
    'team_members': team_members,
    'project_requirements': project_requirements
}

# Run the crew
result = crew.kickoff(inputs=inputs)

# Usage metrics and costs
costs = 0.150 * (crew.usage_metrics['prompt_tokens'] + crew.usage_metrics['completion_tokens']) / 1_000_000
print(f"Total costs: ${costs: .4f}")

# Convert UsageMetrics instance to a DataFrame
df_usage_metrics = pd.DataFrame([crew.usage_metrics])
print(df_usage_metrics)

# Result 
print(result.dict())

# Inspect tasks
tasks = result.dict()['tasks']
df_tasks = pd.DataFrame(tasks)
print(df_tasks.head())

# Inspect milestones
milestones = result.dict()['milestones']
df_milestones = pd.DataFrame(milestones)
print(df_milestones)