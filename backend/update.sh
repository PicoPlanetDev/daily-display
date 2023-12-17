#!/usr/bin/env bash

echo "Updating Daily Display..." # log

# Pull the latest changes
# Hacky way to run as orangepi user
su orangepi -c "git pull"

# Restart the services
echo "Restarting services..." # log
systemctl restart daily-display-frontend.service
systemctl restart daily-display-backend.service
