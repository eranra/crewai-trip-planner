from utils.crew_trace import post_agent_callback
from crew.tools.browser_tools import BrowserTools
from crew.tools.calculator_tools import CalculatorTools
from crew.tools.search_tools import SearchTools
from crewai import Agent, LLM


class TripAgents():

    def city_selection_agent(self):
        return Agent(
            role='City Selection Expert',
            goal='Select the best city based on weather, season, and prices',
            backstory='An expert in analyzing travel data to pick ideal destinations',
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            llm=LLM(model="ollama/llama3.2:1b", base_url="http://localhost:11434"),
            verbose=True,
            step_callback=post_agent_callback
        )

    def local_expert(self):
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city',
            backstory="""A knowledgeable local guide with extensive information
        about the city, it's attractions and customs""",
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            llm=LLM(model="ollama/llama3.2:1b", base_url="http://localhost:11434"),
            verbose=True,
            step_callback=post_agent_callback
        )

    def travel_concierge(self):
        return Agent(
            role='Amazing Travel Concierge',
            goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city""",
            backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
                CalculatorTools.calculate,
            ],
            llm=LLM(model="ollama/llama3.2:1b", base_url="http://localhost:11434"),
            verbose=True,
            step_callback=post_agent_callback
        )
