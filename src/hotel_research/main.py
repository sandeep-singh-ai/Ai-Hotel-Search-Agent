#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from hotel_research.crew import HotelResearch

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    location = input('Enter location to find the best hotel: ')
    miles = input('Enter the miles to search for the hotel: ')
    current_year = str(datetime.now().year)
    inputs = {
        'location': location,
        'miles': miles,
        'current_year': current_year
    }

    try:
        HotelResearch().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
