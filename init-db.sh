#!/bin/bash
set -e

tenetdb --dialect postgresql --username "$POSTGRES_USER" --password "$POSTGRES_PASSWORD" --host localhost --database "$POSTGRES_DB" --port 5432
