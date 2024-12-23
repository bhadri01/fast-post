# Use the official PostgreSQL image as the base
FROM postgres:alpine
RUN apk add --no-cache git postgresql-dev
# Set environment variables (can also be overridden at runtime if needed)
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
# Set environment variables for Postgres (these will be overwritten by Docker Compose)
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB
# Copy any needed initialization or entry scripts, if required (not used here for simplicity)
# COPY ./init-scripts /docker-entrypoint-initdb.d/

# Custom command to replicate the slave database from master
CMD bash -c "\
  until ping -c1 master-db; do sleep 1; done; \
  rm -rf /var/lib/postgresql/data/*; \
  PGPASSWORD=$POSTGRES_PASSWORD pg_basebackup -h master-db -D /var/lib/postgresql/data -U $POSTGRES_USER -Fp -Xs -P -R; \
  echo \"port = 5433\" >> /var/lib/postgresql/data/postgresql.auto.conf; \
  chown -R postgres:postgres /var/lib/postgresql/data; \
  chmod 700 /var/lib/postgresql/data; \
  exec gosu postgres postgres"
