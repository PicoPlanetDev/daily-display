#!/usr/bin/env bash

# Stop the services
systemctl stop daily-display-backend.service
systemctl stop daily-display-frontend.service

# Pull the latest changes
# Hacky way to run as orangepi user
su orangepi -c "git pull"

# Restart the services
systemctl start daily-display-backend.service
systemctl start daily-display-frontend.service
