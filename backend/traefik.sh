#!/bin/sh
# Hostnames of the Traefik services
MASTER_HOSTNAME="traefik"

# Number of ping attempts
PING_ATTEMPTS=1
echo $PING_ATTEMPTS
# Find IP address of master.db
MASTER_IP=$(ping -c $PING_ATTEMPTS $MASTER_HOSTNAME | grep "PING" | awk -F'[()]' '{print $2}')
if [ -z "$MASTER_IP" ]; then
    echo "Failed to get IP address for $MASTER_HOSTNAME"
    exit 1
fi

# Remove existing entries for master.db and slave.db
sed -i '/ master.db/d' /etc/hosts
sed -i '/ slave.db/d' /etc/hosts

# Add the new entries
echo "$MASTER_IP master.db" >> /etc/hosts
echo "$MASTER_IP slave.db" >> /etc/hosts
echo "$MASTER_IP api.db" >> /etc/hosts

echo "IP addresses successfully updated in /etc/hosts:"
echo "$MASTER_IP master.db"
echo "$MASTER_IP slave.db"
echo "$MASTER_IP api.db"