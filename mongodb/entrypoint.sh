#!/bin/bash

# Start MongoDB in the background
mongod --replSet "rs0" --bind_ip_all &

echo "Waiting for MongoDB to start..."
sleep 10  # Adjust this time if needed

echo "Initiating the replica set..."
/usr/local/bin/replica-init.sh

# Keep the container running by waiting for MongoDB process
wait
