
# Task 6: Application Health Checks

## Objective
Configure and verify Docker health checks for the Flask application and its Redis dependency using Docker Compose.

## 1. Application Health Endpoint

The Flask application already has a `/health` endpoint that checks Redis connectivity.

- Returns HTTP 200 when Redis is connected.
- Returns HTTP 503 when Redis is unavailable.
- Reports the application status and Redis connection status.

## 2. Docker Compose Health Check

Configured a health check for the Flask application in `04-docker-compose/docker-compose.yaml`.

Settings:
- Test: Python urllib request to `http://localhost:5000/health`
- Interval: 10 seconds
- Timeout: 5 seconds
- Retries: 3
- Start period: 15 seconds

The Redis service also has a health check using `redis-cli ping`.

The Flask service depends on Redis becoming healthy before its initial startup.

## 3. Build and Deployment

Rebuilt and recreated the Flask application container without recreating Redis:

```powershell
docker compose -f 04-docker-compose/docker-compose.yaml up -d --build --no-deps app
```

Verified the Compose configuration:

```powershell
docker compose -f 04-docker-compose/docker-compose.yaml config --quiet
```

## 4. Endpoint Verification

All three endpoint checks succeeded:

| Endpoint | Result |
|---|---|
| `/` | Application running |
| `/health` | Healthy; Redis connected |
| `/visits` | Returned visit count 9 |

## 5. Failure Simulation

Stopped Redis:

```powershell
docker compose -f 04-docker-compose/docker-compose.yaml stop redis
```

Docker subsequently reported the Flask container as `unhealthy`.

The health endpoint's PowerShell error handler did not capture the HTTP status code, so an HTTP 503 response was not independently confirmed during this test.

## 6. Recovery Verification

Restarted Redis:

```powershell
docker compose -f 04-docker-compose/docker-compose.yaml start redis
```

Verified the services:

```powershell
docker compose -f 04-docker-compose/docker-compose.yaml ps
```

Tested the health endpoint:

```powershell
Invoke-RestMethod http://localhost:5000/health
```

Checked Docker's health status:

```powershell
docker inspect flask-app --format "{{.State.Health.Status}}"
```

Results:
- Redis returned to healthy.
- Flask reported `healthy`.
- The health endpoint reported Redis as connected.

## 7. Conclusion

Successfully configured and tested Docker Compose health checks for the Flask application. Verified normal application operation, detected an unhealthy state when Redis was unavailable, and confirmed recovery after Redis was restarted.
