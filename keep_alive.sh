#!/bin/bash
while true; do
    curl -s "https://photo-organizer.onrender.com" > /dev/null
    echo "Ping sent at $(date)"
    sleep 890   # every 10 minutes
done