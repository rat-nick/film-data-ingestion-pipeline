from dotenv import load_dotenv
import requests
from datetime import timedelta, date
import os
from logging import getLogger
import time

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

    results = []
    max_retries = 5
    backoff_factor = 1

    for attempt in range(max_retries):
        try:
            response = requests.get(DISCOVERY_URL, params=params)
            response.raise_for_status()
            response_data = response.json()
            results.extend(response_data["results"])
            pages = response_data["total_pages"]

            for page in range(2, pages + 1):
                params["page"] = page
                response = requests.get(DISCOVERY_URL, params=params)
                response.raise_for_status()
                results.extend(response.json()["results"])

            break  # Exit the retry loop if the request was successful

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}, attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                params_without_api_key = {k: v for k, v in params.items() if k != "api_key"}
                logger.error(f"Max retries reached. Failed with params: {params_without_api_key}")
                return None

    return results


if __name__ == "__main__":
    print(fetch_films_this_week(date(2021, 1, 1)))