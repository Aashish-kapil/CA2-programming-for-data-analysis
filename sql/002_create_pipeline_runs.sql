CREATE TABLE pipeline_runs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_product TEXT NOT NULL,
    requested_area TEXT NOT NULL,
    request_start DATE NOT NULL,
    request_end DATE NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'running',
    records_received INTEGER,
    records_inserted INTEGER,
    records_skipped INTEGER,
    error_message TEXT,

    CONSTRAINT valid_run_status
        CHECK (status IN ('running', 'succeeded', 'failed')),

    CONSTRAINT valid_request_window
        CHECK (request_end >= request_start),

    CONSTRAINT nonnegative_run_counts
        CHECK (
            records_received >= 0
            AND records_inserted >= 0
            AND records_skipped >= 0
        )
);