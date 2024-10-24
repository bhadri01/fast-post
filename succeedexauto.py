import os
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
GITLAB_ACCESS_TOKEN = os.getenv("GITLAB_ACCESS_TOKEN")

PG_HBA_PATH = "masterdb/init.sh"  # Path to the pg_hba.conf file

def run_command(command, cwd=None):
    """Run a system command and print its output in real-time."""
    try:
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd
        )

        for line in process.stdout:
            print(line.decode(), end="")

        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.cmd}\nExit code: {e.returncode}")
        sys.exit(1)

def update_pg_hba_user():
    """Update the username following 'replication' dynamically in pg_hba.conf."""
    print("Updating pg_hba.conf with the new replication user...")
    
    try:
        with open(PG_HBA_PATH, "r") as file:
            lines = file.readlines()

        # Update the line containing 'replication'
        with open(PG_HBA_PATH, "w") as file:
            for line in lines:
                if line.startswith("host") and "replication" in line:
                    # Replace the word following 'replication' with POSTGRES_USER
                    parts = line.split()
                    if len(parts) > 2:
                        parts[2] = POSTGRES_USER  # Update the username dynamically
                    line = "    ".join(parts) + "\n"  # Maintain proper spacing
                file.write(line)

        print("pg_hba.conf updated successfully!")
    except Exception as e:
        print(f"Failed to update pg_hba.conf: {e}")
        sys.exit(1)


def build_masterDB():
    """Build the master DB Docker container."""
    print("Building the master DB container...")
    run_command(
        f"docker compose build master-db --build-arg POSTGRES_USER={POSTGRES_USER} "
        f"--build-arg POSTGRES_PASSWORD={POSTGRES_PASSWORD} "
        f"--build-arg POSTGRES_DB={POSTGRES_DB} --no-cache"
    )

def build_slaveDB():
    """Build the slave DB Docker container."""
    print("Building the slave DB container...")
    run_command(
        f"docker compose build slave-db --build-arg POSTGRES_USER={POSTGRES_USER} "
        f"--build-arg POSTGRES_PASSWORD={POSTGRES_PASSWORD} "
        f"--build-arg POSTGRES_DB={POSTGRES_DB} --no-cache"
    )

def build_backend():
    """Build the backend Docker container."""
    print("Building the backend container...")
    run_command(
        f"docker compose build backend --build-arg GITLAB_ACCESS_TOKEN={GITLAB_ACCESS_TOKEN} "
        f"--build-arg POSTGRES_USER={POSTGRES_USER} " 
        f"--build-arg POSTGRES_DB={POSTGRES_DB} --no-cache"
    )

def docker_compose_up():
    """Run docker-compose up to start all services."""
    print("Starting the Docker Compose services...")
    run_command("docker compose up -d")

def execute_in_container():
    """Execute a script inside the backend container."""
    print("Executing script inside the backend container...")
    command = "docker exec --user root backend /usr/local/bin/traefik.sh"
    run_command(command)

def main():
    """Main entry point of the script."""
    print("Running the Docker automation script...")

    # Step 1: Update pg_hba.conf with the new user
    update_pg_hba_user()

    # Step 2: Build the services
    build_masterDB()
    build_backend()
    build_slaveDB()

    # Step 3: Bring up the docker-compose services
    docker_compose_up()

    # Step 4: Execute script inside the backend container (Optional)
    # execute_in_container()

    print("All services are up and running!")

if __name__ == "__main__":
    main()
