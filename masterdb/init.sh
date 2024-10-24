#!/bin/bash
# Append to pg_hba.conf after the data directory is initialized
if [ -f "/var/lib/postgresql/data/pg_hba.conf" ]; then
  echo "host    replication    $POSTGRES_USER    0.0.0.0/0    trust" >> /var/lib/postgresql/data/pg_hba.conf
fi