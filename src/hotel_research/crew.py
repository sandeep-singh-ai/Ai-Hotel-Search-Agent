from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from dotenv import load_dotenv

from hotel_research.tools.hotel_search import hotel_search_tool

load_dotenv()


@CrewBase
class HotelResearch():
    """HotelResearch crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def travel_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_agent'],
            tools=[hotel_search_tool],
            verbose=True
        )

    @agent
    def tourist_guide(self) -> Agent:
        # No tools: the guide works only from the travel agent's results.
        return Agent(
            config=self.agents_config['tourist_guide'],
            tools=[],
            verbose=True
        )

    @task
    def travel_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['travel_agent_task'],
        )

    @task
    def tourist_guide_task(self) -> Task:
        return Task(
            config=self.tasks_config['tourist_guide_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the HotelResearch crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
