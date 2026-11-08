#!/usr/bin/env python
import warnings
from datetime import date, timedelta

from hotel_research.crew import HotelResearch

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def _ask_text(prompt: str, default: str = "") -> str:
    while True:
        value = input(prompt).strip()
        if value or default:
            return value or default
        print("This field is required.")


def _ask_miles() -> float:
    while True:
        raw = input("Enter the search radius in miles: ").strip()
        try:
            miles = float(raw)
        except ValueError:
            print("Enter a number, for example 5.")
            continue
        if miles > 0:
            return miles
        print("Radius must be greater than 0.")


def _ask_date(prompt: str, default: date, earliest: date) -> date:
    while True:
        raw = input(f"{prompt} (YYYY-MM-DD, default {default.isoformat()}): ").strip()
        if not raw:
            return default
        try:
            value = date.fromisoformat(raw)
        except ValueError:
            print("Use the format YYYY-MM-DD.")
            continue
        if value >= earliest:
            return value
        print(f"Date must be on or after {earliest.isoformat()}.")


def run():
    """
    Run the crew.
    """
    location = _ask_text("Enter location to find the best hotel: ")
    miles = _ask_miles()
    today = date.today()
    check_in = _ask_date("Enter the check-in date", today + timedelta(days=1), today)
    check_out = _ask_date("Enter the check-out date", check_in + timedelta(days=1), check_in + timedelta(days=1))
    preferences = _ask_text(
        "Any preferences (budget, amenities, vibe)? Press Enter to skip: ",
        default="no specific preferences; balance price, rating and distance",
    )

    inputs = {
        'location': location,
        'miles': miles,
        'check_in_date': check_in.isoformat(),
        'check_out_date': check_out.isoformat(),
        'preferences': preferences,
    }

    HotelResearch().crew().kickoff(inputs=inputs)
