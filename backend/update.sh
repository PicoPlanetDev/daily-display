#!/usr/bin/env bash

# Pull the latest changes
# Hacky way to run as orangepi user
su orangepi -c "git pull"

# Restart the services
systemctl restart daily-display-frontend.service
systemctl restart daily-display-backend.service
