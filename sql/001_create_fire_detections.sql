CREATE TABLE fire_detections (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_product TEXT NOT NULL,
    satellite TEXT NOT NULL,
    instrument TEXT NOT NULL,
    acquired_at TIMESTAMPTZ NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    bright_ti4 DOUBLE PRECISION,
    bright_ti5 DOUBLE PRECISION ,
    frp DOUBLE PRECISION ,
    track DOUBLE PRECISION ,
    scan DOUBLE PRECISION ,
    confidence TEXT,
    version TEXT,
    daynight TEXT,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_fire_observation UNIQUE (
        source_product,
        satellite,
        instrument,
        acquired_at,
        latitude,
        longitude
    )
);