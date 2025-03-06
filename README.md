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
-   `schema.sql`: SQL schema for the `film_metadata` table.
-   `.gitignore`: Specifies files and directories to be ignored by Git.
-   `LICENSE`: License information for the project.

## Getting Started

### Prerequisites

-   Docker
-   Docker Compose

### Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/film-data-ingestion-pipeline.git
    cd film-data-ingestion-pipeline
    ```

2. Create a `.env` file with your TMDB API key:

    ```sh
    echo "TMDB_API_KEY=your_api_key_here" > .env
    ```

3. Start the services using Docker Compose:

    ```sh
    docker-compose up -d
    ```

4. Access the Airflow webserver at `http://localhost:8080` and log in with the
   default credentials (`airflow`/`airflow`).

## Usage

The pipeline is scheduled to run weekly and will:

1. Fetch film data from TMDB.
2. Process and save the data to a temporary file.
3. Load the data into the PostgreSQL database.
4. Clean up temporary files.

## License

This project is licensed under the BSD 3-Clause License. See the
[LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any
changes.

## Contact

For any inquiries, please contact Nikola Ratinac.
