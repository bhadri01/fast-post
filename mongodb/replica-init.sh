#!/bin/bash

echo "Waiting for MongoDB instances to be available..."

# Loop to wait for all instances to be reachable
for i in {1..10}; do
  if mongosh --host mongo2:27017 --eval "db.adminCommand('ping')" &&
     mongosh --host mongo3:27017 --eval "db.adminCommand('ping')"; then
    echo "All MongoDB instances are up and running!"
    break
  else
    echo "Waiting for MongoDB instances to start... ($i/10)"
    sleep 5
  fi
done

echo "Initiating the replica set..."
mongosh --host localhost:27017 --eval 'rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
});'

echo "Replica set initiated."
