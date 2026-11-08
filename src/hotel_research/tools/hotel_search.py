import json
import math
import os
from datetime import date, timedelta

import serpapi
from crewai.tools import tool

MAX_RESULTS = 8


def _resolve_dates(check_in_date: str, check_out_date: str) -> tuple[str, str]:
    """Fill missing dates: check-in defaults to tomorrow, check-out to one night after check-in."""
    check_in = date.fromisoformat(check_in_date) if check_in_date else date.today() + timedelta(days=1)
    check_out = date.fromisoformat(check_out_date) if check_out_date else check_in + timedelta(days=1)
    if check_out <= check_in:
        raise ValueError(f"check_out_date {check_out} must be after check_in_date {check_in}")
    return check_in.isoformat(), check_out.isoformat()


def _haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 3958.8  # Earth radius in miles
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _geocode(client: serpapi.Client, location: str) -> tuple[float, float] | None:
    """Look up the center point of the location with SerpAPI's Google Maps engine."""
    results = client.search({"engine": "google_maps", "q": location, "type": "search"})
    place = results.get("place_results") or {}
    coords = place.get("gps_coordinates")
    if not coords:
        local = results.get("local_results") or []
        coords = local[0].get("gps_coordinates") if local else None
    if not coords or "latitude" not in coords or "longitude" not in coords:
        return None
    return coords["latitude"], coords["longitude"]


def _summarize(hotel: dict, center: tuple[float, float] | None) -> dict:
    coords = hotel.get("gps_coordinates") or {}
    distance = None
    if center and "latitude" in coords and "longitude" in coords:
        distance = round(_haversine_miles(*center, coords["latitude"], coords["longitude"]), 2)
    return {
        "name": hotel.get("name"),
        "price_per_night": (hotel.get("rate_per_night") or {}).get("lowest"),
        "total_price": (hotel.get("total_rate") or {}).get("lowest"),
        "rating": hotel.get("overall_rating"),
        "reviews": hotel.get("reviews"),
        "hotel_class": hotel.get("hotel_class"),
        "amenities": (hotel.get("amenities") or [])[:10],
        "distance_miles": distance,
        "link": hotel.get("link"),
    }


@tool("hotel_search_tool")
def hotel_search_tool(location: str, check_in_date: str = "", check_out_date: str = "", miles: float = 0) -> str:
    """Search Google Hotels for a location. Dates use YYYY-MM-DD; if omitted, check-in is tomorrow
    and check-out is one night later. If miles > 0, only hotels within that radius of the location
    are returned. Returns JSON with the dates searched and a list of hotels (name, price, rating,
    reviews, class, amenities, distance_miles, link), or an error message."""
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Error: SERPAPI_API_KEY is not set. Add it to .env."

    try:
        check_in_date, check_out_date = _resolve_dates(check_in_date, check_out_date)
    except ValueError as exc:
        return f"Error: invalid dates: {exc}"

    try:
        miles = float(miles or 0)
    except (TypeError, ValueError):
        return f"Error: miles must be a number, got {miles!r}"

    client = serpapi.Client(api_key=api_key)
    try:
        results = client.search({
            "engine": "google_hotels",
            "q": location,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
        })
        center = _geocode(client, location) if miles > 0 else None
    except Exception as exc:
        return f"Error: hotel search failed: {str(exc).replace(api_key, '[redacted]')}"

    hotels = [_summarize(h, center) for h in results.get("properties") or []]
    note = None
    if miles > 0:
        if center is None:
            note = "Could not geocode the location; radius filter not applied and distances are unknown."
        else:
            hotels = [h for h in hotels if h["distance_miles"] is not None and h["distance_miles"] <= miles]
            hotels.sort(key=lambda h: h["distance_miles"])
            if not hotels:
                note = f"No hotels in the first page of results fall within {miles} miles."

    return json.dumps({
        "location": location,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "radius_miles": miles or None,
        "note": note,
        "hotels": hotels[:MAX_RESULTS],
    })
