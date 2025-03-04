CREATE TABLE IF NOT EXISTS film_metadata(
    id SERIAL PRIMARY KEY,
    is_adult BOOLEAN,
    genres TEXT,
    external_id TEXT NOT NULL,
    source TEXT NOT NULL,
    original_language TEXT,
    original_title TEXT,
    title TEXT NOT NULL,
    backdrop_path TEXT,
    overview TEXT,
    poster_path TEXT,
    release_date DATE
);

ALTER TABLE film_metadata 
ADD CONSTRAINT unique_source_external_id UNIQUE (source, external_id);