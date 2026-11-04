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
---
# Day 2 – Service Dependency, Recovery and Troubleshooting
Date: 4 November 2026
Project: DevOps Intern Tasks
Branch: feature/docker-compose-day2
## 13. Objective
The objective of Day 2 was to test how the Flask application behaves when its supporting Redis service becomes unavailable, practise service recovery, and troubleshoot application response and worker timeout issues.
## 14. Testing Service Dependency and Recovery
I stopped the Redis service using:
docker compose stop redis
I inspected the running services with:
docker compose ps
Redis stopped while the Flask application remained running.
I tested the application health endpoint and observed an empty response from the application. I inspected the application logs to investigate the problem.
I then restarted Redis:
docker compose start redis
I verified Redis connectivity using:
docker compose exec redis redis-cli ping
Result: Redis returned PONG, confirming that the Redis service was responding.
## 15. Troubleshooting Gunicorn Worker Timeouts
During testing, some requests to the /health and /visits endpoints timed out or returned empty responses.
I inspected the application logs using:
docker compose logs app --tail 60
The logs showed Gunicorn worker timeout messages and worker restarts.
I reviewed app/routes.py and the Dockerfile. The Redis client already had connection and socket timeout settings configured.
To make Gunicorn's resource usage and request logging more explicit, I updated its command in the Dockerfile to use:
- One worker.
- A 10-second worker timeout.
- Access logging to standard output.
- Error logging to standard output.
- The application factory app:create_app().
The updated Gunicorn command was:
CMD ["gunicorn", "--workers", "1", "--timeout", "10", "--access-logfile", "-", "--error-logfile", "-", "--bind", "0.0.0.0:5000", "app:create_app()"]
I rebuilt and restarted the application using:
docker compose up -d --build app
Result: The application image built successfully and the Flask container started.
## 16. Final Application Testing
I tested all application endpoints using curl:
curl --max-time 5 http://localhost:5000/
curl --max-time 5 http://localhost:5000/health
curl --max-time 5 http://localhost:5000/visits
curl --max-time 5 http://localhost:5000/visits
Observed results:
- The home endpoint returned the application running message.
- The health endpoint returned healthy status and Redis connected.
- The first visits request returned a counter value of 7.
- The second visits request returned a counter value of 8.
Result: All four requests completed successfully within the five-second limit. The increasing counter confirmed that Redis was storing and incrementing visit data.
## 17. Log Verification
I inspected recent application logs using:
docker compose logs --since=5m app
The logs showed Gunicorn starting successfully and listening on port 5000.
They also recorded successful HTTP 200 responses for:
- GET /
- GET /health
- GET /visits
- GET /visits
No new worker timeout errors appeared in these fresh logs.
## 18. Troubleshooting Lessons
During this exercise, I learned how stopping a supporting service can affect an application that depends on it. I also practised inspecting container logs, checking Redis connectivity, restarting services, rebuilding an application image, and verifying endpoint responses.
The intermittent Gunicorn worker timeouts required additional investigation. I updated the Gunicorn configuration and enabled request logging. The subsequent tests and fresh logs showed successful responses, although the original cause of the intermittent timeouts was not conclusively established.
## 19. Day 2 Learning Outcome
I gained practical experience troubleshooting a multi-container application when a dependent service becomes unavailable. I learned how to inspect application and service logs, verify Redis connectivity, recover a stopped service, rebuild an application image, and confirm successful communication between Flask and Redis.
Day 2 Status: Troubleshooting and endpoint verification completed. Documentation and GitHub submission pending.
