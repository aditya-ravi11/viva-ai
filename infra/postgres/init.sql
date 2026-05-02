-- Bootstrap script for local Postgres (mounted into pgvector image's
-- /docker-entrypoint-initdb.d/). Runs once on first container start.
-- Production (Railway) requires a one-time `CREATE EXTENSION vector;`
-- run manually via the Railway DB shell.

CREATE EXTENSION IF NOT EXISTS vector;
