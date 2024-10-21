import logging
from logging import INFO

import streamlit as st
from crewai import Crew, Process, LLM

from crew.trip_agents import TripAgents
from crew.trip_tasks import TripTasks

logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=INFO)
logging.info("Starting app")


class TripCrew:

    def __init__(self, origin, cities, date_range, interests):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.date_range = date_range
        self.output_placeholder = st.empty()

    def run(self):
        logging.info("Run TripCrew - start")
        agents = TripAgents()
        tasks = TripTasks()

        logging.info("Run TripCrew - define agents")
        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        logging.info("Run TripCrew - define tasks")
        identify_task = tasks.identify_task(
            city_selector_agent,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )

        gather_task = tasks.gather_task(
            local_expert_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        plan_task = tasks.plan_task(
            travel_concierge_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        logging.info("Run TripCrew - define crew")
        crew = Crew(
            # agents=[
            #     city_selector_agent, local_expert_agent, travel_concierge_agent
            # ],
            # tasks=[identify_task, gather_task, plan_task],
            # verbose=True
            agents=[
                city_selector_agent
            ],
            tasks=[identify_task],
            process=Process.sequential,
            verbose=True,
            # cache=True,
            # memory=True
            # planning=True,
            # planning_llm=LLM(model="ollama/llama3.2:1b", base_url="http://localhost:11434"),
        )

        logging.info("Run TripCrew - Crew kickoff")
        result = crew.kickoff()
        logging.info("Run TripCrew - Post Crew kickoff")
        self.output_placeholder.markdown(result)

        logging.debug(f"Run TripCrew - result = {result}")
        return result
