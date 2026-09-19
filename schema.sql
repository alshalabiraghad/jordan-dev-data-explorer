CREATE TABLE indicators (
    indicator_code TEXT PRIMARY KEY,
    indicator_name TEXT NOT NULL,
    unit TEXT,
    source TEXT
);

CREATE TABLE locations (
    location_name TEXT PRIMARY KEY,
    location_type TEXT NOT NULL
);

CREATE TABLE observations (
    id SERIAL PRIMARY KEY,
    indicator_code TEXT REFERENCES indicators(indicator_code),
    location_name TEXT REFERENCES locations(location_name),
    year INT NOT NULL,
    value FLOAT
);

ALTER TABLE observations ADD CONSTRAINT unique_observation UNIQUE (indicator_code, location_name, year);