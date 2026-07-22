# Migrations

This folder is reserved for Alembic migration scripts in the next database phase.

Planned flow:

1. Initialize Alembic
2. Point `sqlalchemy.url` at `DATABASE_URL`
3. Autogenerate revisions from `database.models`
4. Apply migrations to PostgreSQL in production