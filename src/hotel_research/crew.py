from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.tools import tool
from crewai_tools import SerperScrapeWebsiteTool
import json
import os
from datetime import date, timedelta

import serpapi
from dotenv import load_dotenv

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
            tools=[self.hotel_search_tool],
            verbose=True
        )

    @agent
    def tourist_guide(self) -> Agent:
        return Agent(
            config=self.agents_config['tourist_guide'],
            tools=[self.hotel_search_tool],
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

    @tool('hotel_search_tool')
    def hotel_search_tool(location: str, check_in_date: str = "", check_out_date: str = "") -> str:
        """Search for hotels in a location. Dates are optional and use YYYY-MM-DD."""
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            raise ValueError("SERPAPI_API_KEY is not set")

        if not check_in_date or not check_out_date:
            check_in = date.today() + timedelta(days=1)
            check_out = check_in + timedelta(days=1)
            check_in_date = check_in_date or check_in.isoformat()
            check_out_date = check_out_date or check_out.isoformat()

        client = serpapi.Client(api_key=api_key)
        try:
            results = client.search({
                "engine": "google_hotels",
                "q": location,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
            })
        except Exception as exc:
            raise RuntimeError(str(exc).replace(api_key, "[redacted]")) from None

        properties = results.get("properties") or []
        summary = [
            {
                "name": hotel.get("name"),
                "price": (hotel.get("rate_per_night") or {}).get("lowest"),
                "rating": hotel.get("overall_rating"),
                "reviews": hotel.get("reviews"),
            }
            for hotel in properties[:8]
        ]
        return json.dumps(summary)


    @crew
    def crew(self) -> Crew:
        """Creates the HotelResearch crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
