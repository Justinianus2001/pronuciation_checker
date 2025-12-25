# Docker Compose Simplification

## Changes Made

### Removed Nginx Service
- Simplified `docker-compose.yml` to single service
- Removed Nginx reverse proxy
- Flask app now exposed directly on port 5000

### Updated Configuration

#### docker-compose.yml
- **Before**: 2 services (web + nginx) on ports 80/443
- **After**: 1 service (web) on port 5000
- Added cleanup environment variables
- Removed Nginx dependencies

#### Dockerfile
- Added `curl` for health checks
- Updated health check to use curl instead of Python

#### deploy_docker.sh
- Updated URLs from `localhost` to `localhost:5000`
- Added storage stats endpoint to output

## New Docker Setup

### Single Service Architecture
```
Client Request (Port 5000)
    ↓
Gunicorn (Flask App)
    ↓
Application Logic
```

### Access Points
- **Application**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/v1/health-check
- **Storage Stats**: http://localhost:5000/api/v1/storage-stats

### Environment Variables
All cleanup variables now passed through docker-compose:
```yaml
environment:
  - CLEANUP_ENABLED=${CLEANUP_ENABLED:-true}
  - CLEANUP_MAX_AGE_DAYS=${CLEANUP_MAX_AGE_DAYS:-7}
  - CLEANUP_INTERVAL_HOURS=${CLEANUP_INTERVAL_HOURS:-24}
```

## Usage

### Deploy
```bash
bash scripts/deploy_docker.sh
```

### Access Application
```bash
# Health check
curl http://localhost:5000/api/v1/health-check

# Storage stats
curl http://localhost:5000/api/v1/storage-stats

# Test endpoint
curl -X POST http://localhost:5000/api/v1/analyze-pronunciation-error \
  -F "audio=@test.mp3" \
  -F "text=Hello world"
```

### Manage
```bash
# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

## Benefits of Simplified Setup

✅ **Simpler**: One service instead of two  
✅ **Faster**: No reverse proxy overhead  
✅ **Easier**: Less configuration to manage  
✅ **Lighter**: Smaller resource footprint  
✅ **Cleaner**: Fewer moving parts  

## Note

If you need Nginx for production (SSL, load balancing, etc.), you can:
1. Use the old `nginx.conf` file
2. Add Nginx service back to `docker-compose.yml`
3. Or use a separate Nginx instance/container

For development and simple deployments, direct access to Flask/Gunicorn is sufficient!
