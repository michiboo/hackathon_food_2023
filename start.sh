#!/bin/bash

# Start the database container
docker stop my-flask-app
docker rm my-flask-app
# docker run -d --name my-db-container -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -p 5432:5432 postgres:latest

# Wait for the database container to initialize
sleep 5

# Start the Flask application container
docker build -t backendapp .
docker run -d --name my-flask-app -p 5000:5000 -t backendapp

echo "Application and database containers started successfully."