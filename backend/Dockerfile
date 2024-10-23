FROM python:3.11-alpine

# Define the GitLab access token as a build argument
ARG GITLAB_ACCESS_TOKEN
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

# Install necessary packages
RUN apk add --no-cache git postgresql-dev shadow docker busybox-extras  

# Create the new user 'succeedEx' and set up environment
RUN useradd -m succeedEx 
RUN usermod -aG docker succeedEx

# Set necessary environment variables
ENV POSTGRESQL_DATABASE_MASTER_URL="postgresql+asyncpg://$POSTGRES_USER:$POSTGRES_PASSWORD@master.db/$POSTGRES_DB" \
    POSTGRESQL_DATABASE_SLAVE_URL="postgresql+asyncpg://$POSTGRES_USER:$POSTGRES_PASSWORD@master.db/$POSTGRES_DB"

# Set the working directory to the new user’s home
WORKDIR /home/succeedEx/

# Switch to the succeedEx user for the next operations
USER succeedEx
RUN chown succeedEx:succeedEx /home/succeedEx/
# Clone the GitHub repository into the user’s home directory
# RUN git clone https://oauth2:$GITLAB_ACCESS_TOKEN@gitlab.com/succeedex/backend-crm.git /home/succeedEx/backend/
RUN git clone https://github.com/Anish13kumar/Fastapi_PostgreSQL /home/succeedEx/backend/

# Switch back to root to install dependencies
RUN pip install -r /home/succeedEx/backend/requirements.txt
RUN pip install pika

USER root
# Copy and configure the Traefik script
COPY traefik.sh /usr/local/bin/traefik.sh
RUN chmod +x /usr/local/bin/traefik.sh
# Set the succeedEx user as the default for running the container
# Default command to run the container
USER succeedEx
CMD ["tail", "-f", "/dev/null"]

