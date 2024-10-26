FROM mongo:latest

# Copy the replica set initiation script into the container
COPY replica-init.sh /usr/local/bin/replica-init.sh

# Make the script executable
RUN chmod +x /usr/local/bin/replica-init.sh

# Expose the MongoDB port
EXPOSE 27017

# Copy the custom entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Use the custom entrypoint to start the processes
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
