from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperScrapeWebsiteTool


@CrewBase
class HotelResearch():
    """HotelResearch crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def travel_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_agent'],
            tools=[SerperScrapeWebsiteTool()],
            verbose=True
        )

    @agent
    def tourist_guide(self) -> Agent:
        return Agent(
            config=self.agents_config['tourist_guide'],
            tools=[SerperScrapeWebsiteTool()],
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
