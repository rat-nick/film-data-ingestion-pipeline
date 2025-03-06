from dotenv import load_dotenv
import requests
from datetime import timedelta, date
import os
from logging import getLogger

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
DISCOVERY_URL = "https://api.themoviedb.org/3/discover/movie"
GENRES_URL = "https://api.themoviedb.org/3/genre/movie/list"

logger = getLogger(__name__)


def fetch_genres():
    params = {
        "api_key": API_KEY
    }
    
    response = requests.get(GENRES_URL, params=params)
    
    if not response.ok:
        return None
    
    genres = {genre["id"]: genre["name"] for genre in response.json()["genres"]}
    return genres


def fetch_films_this_week(start_date):
    end_date = start_date + timedelta(days=7)

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    
    params = {
        "api_key": API_KEY,
        "primary_release_date.gte": start_date,
        "primary_release_date.lte": end_date,
        "sort_by": "popularity.desc",
    }
    logger.info(f"Fetching films from {start_date} to {end_date}")
    
    response = requests.get(DISCOVERY_URL, params=params)

    if not response.ok:
        return None
    
    response = response.json()
    
    pages = response["total_pages"]
    results = response["results"]
    
    for page in range(2, pages + 1):
        params["page"] = page
        response = requests.get(DISCOVERY_URL, params=params)
        results.extend(response.json()["results"])
    print(type(results))
    return results


if __name__ == "__main__":
    print(fetch_films_this_week(date(2021, 1, 1)))