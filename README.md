# Film Data Ingestion Pipeline

This project is designed to fetch, process, and store film metadata from The
Movie Database (TMDB) using Apache Airflow. The pipeline consists of several
components including data fetching, processing, and loading into a PostgreSQL
database.

## Project Structure

-   `dags/`: Contains the Airflow DAGs.
    -   `weekly_film_discovery_dag.py`: Defines the DAG for discovering and
        processing films on a weekly basis.
-   `dags/utils/`: Contains utility scripts.
    -   `films.py`: Contains functions to fetch film data and genres from TMDB.
-   `docker-compose.yaml`: Docker Compose configuration to set up the Airflow
    and PostgreSQL services.
-   `schema.sql`: SQL schema for the database containing the production data.

## Getting Started

### Prerequisites

-   Docker
-   Docker Compose
-   TMDB API key

### Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/film-data-ingestion-pipeline.git
    cd film-data-ingestion-pipeline
    ```

2. Create a `.env` and run the following commands:

    ```sh
    touch .env
    echo "TMDB_API_KEY=<your_api_key_here>" >> .env
    echo "AIRFLOW_UID=50000" >> .env
    echo "AIRFLOW_GID=0" >> .env
    ```

3. Start the services using Docker Compose:

    ```sh
    docker-compose up -d
    ```

4. Access the Airflow webserver at `http://localhost:8080` and log in with the
   default credentials (`airflow`/`airflow`).

5. Add a new connection from the Admin tab. You should use the following
   parameters:

    | Parameter       | Value               |
    | --------------- | ------------------- |
    | Connection Id   | `media-metadata-db` |
    | Connection Type | Postgres            |
    | Host            | `media-db`          |
    | Schema          | `media`             |
    | Login           | `media`             |
    | Password        | `media`             |
    | Port            | `5432`              |

Of course, you could use a DBaaS like [neon](https://neon.tech), but the free
tier is limited for the data that will be ingested. Just don't forget to change
the connection parameters.

6. Enable the `weekly_film_discovery` DAG and voila!

## Usage

The pipeline is scheduled to run weekly and will:

1. Fetch film data from TMDB.
2. Process and save the data to a temporary file.
3. Load the data into the PostgreSQL database.
4. Clean up temporary files.

### Extra

If you wish to explore the media database, the port on the host is `15432`

## Disclaimer

- This project **uses the TMDB API** but is **not endorsed or certified by TMDB**.
- TMDB data is used in compliance with their [Terms of Use](https://www.themoviedb.org/terms-of-use).
- This project is **for personal and educational purposes only** and does **not** redistribute or resell TMDB data.

For more information, visit **[TMDB's official website](https://www.themoviedb.org/)**.

## License

This project is licensed under the BSD 3-Clause License. See the
[LICENSE](./LICENSE) file for details.
