Task 4: Docker Compose
Day 1 – Multi-Container Application Setup
Date: 4 November 2026
Project: DevOps Intern Tasks
Branch: feature/docker-compose
1. Objective
The objective of Day 1 was to learn how to use Docker Compose to define, build, and run a multi-container application.
I created a Flask web application connected to a Redis service. Docker Compose was used to manage both services, their networking, environment variables, health checks, and persistent storage.
2. Project Structure
The following files and directories were created inside 04-docker-compose/:
04-docker-compose/
├── app/
│   ├── __init__.py
│   └── routes.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yaml
├── docker-compose.md
└── requirements.txt
3. Application Configuration
The Flask application provides three endpoints:
/ – Displays a message confirming that the application is running.
/health – Checks the application’s connection to Redis and returns its health status.
/visits – Increments and returns a visit counter stored in Redis.
The application uses the Python packages listed in requirements.txt:
Flask
redis
gunicorn
4. Dockerfile
A Dockerfile was created to package the Flask application into a Docker image.
The configuration uses:
python:3.12-slim as the base image.
/app as the working directory.
requirements.txt to install dependencies.
The application source code copied into the image.
Port 5000 exposed for the Flask application.
Gunicorn to serve the application.
5. Docker Compose Configuration
The docker-compose.yaml file defines two services:
Flask application (app)
Builds from the local Dockerfile.
Publishes port 5000.
Receives Redis connection settings through environment variables.
Depends on Redis becoming healthy before starting.
Redis (redis)
Uses the redis:7-alpine image.
Publishes port 6379.
Uses a named volume called redis-data.
Runs with append-only persistence enabled.
Includes a health check using redis-cli ping.
The Compose configuration also includes:
A default Docker network for communication between services.
A restart policy of unless-stopped.
A Redis health check configured with a 5-second interval, 3-second timeout, and 5 retries.
6. Environment Variables and Git Ignore
Created .env.example with the following placeholder configuration:
REDIS_HOST=redis
REDIS_PORT=6379
The .gitignore file excludes .env, Python cache files, and virtual environment directories to avoid committing local configuration and generated files.
7. Commands Executed
The following commands were used during the exercise:
Validate the Compose configuration:
docker compose config
Result: The configuration was successfully validated.
Inspect existing containers:
docker ps -a
Result: Existing containers from previous exercises were inspected. They were preserved and not deleted.
Build and start the services:
docker compose up -d --build
Result:
Flask image built successfully.
Docker network created.
Redis named volume created.
Redis container started and became healthy.
Flask container started successfully.
Check service status:
docker compose ps
Result: Both services were running. Redis reported a healthy status.
Restart the services:
docker compose restart
Result: Both services restarted successfully.
8. Application Testing
The application was tested through a web browser.
Endpoint
Expected result
Observed result
http://localhost:5000/
Application running message
Passed
http://localhost:5000/health
Healthy status and Redis connected
Passed
http://localhost:5000/visits
Increasing visit counter
Passed
The health endpoint returned:
{
 "redis": "connected",
 "status": "healthy"
}
The visits endpoint returned a JSON response containing the visit count.
9. Redis Data Persistence Test
To verify persistence, I accessed the /visits endpoint and increased the counter.
The counter showed 2 before restarting the services.
I then executed:
docker compose restart
After the restart, I refreshed the /visits endpoint. The counter continued to 3 rather than resetting to 1.
Result: The test confirmed that Redis retained its visit counter after the container restart. The named volume redis-data provides persistent storage for Redis data.
10. Troubleshooting and Observations
The existing Docker environment contained containers from earlier projects. I inspected them before starting the new services to avoid disturbing previous work.
The new Compose project used distinct container names: flask-app and redis-service.
No configuration or startup errors were observed during the Day 1 build and testing process.
11. Verified Deliverables
☑ Flask application created.
☑ Redis service configured.
☑ Dockerfile created.
☑ Docker Compose configuration created.
☑ Environment example file created.
☑ Git ignore file configured.
☑ Compose configuration validated.
☑ Both containers built and started successfully.
☑ Redis health check passed.
☑ Application endpoints tested successfully.
☑ Redis persistence verified after container restart.
12. Day 1 Learning Outcome
Today, I learned how Docker Compose simplifies the management of multi-container applications. I gained practical experience defining services in YAML, configuring service dependencies, connecting a Flask application to Redis, using health checks, and managing persistent data with named volumes.
I also learned how to validate a Compose configuration, build and start multiple services together, inspect their status, test application endpoints, and verify that application data survives a container restart.
Day 1 Status: Completed.
