#!/usr/bin/env bash

# Stop the services
systemctl stop daily-display-backend.service
systemctl stop daily-display-frontend.service

# Pull the latest changes
git pull

# Restart the services
systemctl start daily-display-backend.service
systemctl start daily-display-frontend.service
