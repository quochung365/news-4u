# Raspberry Pi 4 Deployment Guide

This guide will help you deploy News 4U on a Raspberry Pi 4 or later, with:
- **Backend API** accessible at `/api`
- **Frontend** accessible at `/news`
- **Nginx** as reverse proxy

## Quick Reference

**Key Configuration:**
- Backend runs on `127.0.0.1:8000` (internal only)
- Frontend runs on `127.0.0.1:3000` (internal only)
- Nginx proxies `/api/*` → Backend
- Nginx proxies `/news/*` → Frontend
- Frontend `basePath`: `/news` (build-time)
- Frontend `API_URL`: `/api` (build-time)

**Nginx Config File:** `nginx.conf` (in project root)

**Important for Local Testing:**
- ✅ **DO:** Access frontend at `http://localhost:3000/` (root path)
- ✅ **DO:** Access backend at `http://localhost:8000/api`
- ❌ **DON'T:** Access `http://localhost:3000/news` directly (Next.js basePath handles this internally)
- ❌ **DON'T:** Access `http://localhost:3000/api` (API is on port 8000, not 3000)

**Note:** With `basePath=/news`, Next.js serves the app at root `/`, and all internal routes are automatically prefixed with `/news`. For production, nginx handles the `/news` path routing.

## Prerequisites

- Raspberry Pi 4 or later (4GB RAM minimum recommended)
- Raspberry Pi OS (64-bit recommended) or Ubuntu Server
- Docker and Docker Compose installed
- Nginx installed
- Basic knowledge of Linux command line

## Step 1: System Preparation

### 1.1 Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose -y

# Log out and log back in for group changes to take effect
```

### 1.3 Install Nginx

```bash
sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

## Step 2: Clone and Prepare the Project

### 2.1 Clone Repository

```bash
cd ~
git clone <your-repo-url> news-4u
cd news-4u
```

### 2.2 Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
nano .env
```

Add the following:

```env
DATABASE_URL=sqlite:///./news_4u.db
SCHEDULE_ENABLE=true
```

Save and exit (Ctrl+X, then Y, then Enter).

### 2.3 Configure Frontend API URL and Base Path

Create a `.env.local` file in the `frontend` directory:

```bash
cd ../frontend
nano .env.local
```

Add:

```env
NEXT_PUBLIC_API_URL=/api
NEXT_PUBLIC_BASE_PATH=/news
```

**Important:** 
- Use `/api` (relative path) for production with nginx. The code handles this correctly - when `NEXT_PUBLIC_API_URL=/api`, it's converted to empty string since API paths already include `/api/news/...`.
- For local testing WITHOUT nginx, you'll need to rebuild with `NEXT_PUBLIC_API_URL=http://localhost:8000` (see Step 6.2).
- Set `NEXT_PUBLIC_BASE_PATH=/news` so Next.js knows it's being served from the `/news` path.

## Step 3: Build and Run Docker Containers

### 3.1 Build Images

From the project root directory:

```bash
cd ~/news-4u

# Build backend
cd backend
docker build -t news-4u-backend .

# Build frontend (with basePath and API URL as build arguments)
cd ../frontend
docker build \
  --build-arg NEXT_PUBLIC_API_URL=/api \
  -t news-4u-frontend .
```

**Important:** The `basePath` is a build-time configuration in Next.js, so it must be set during the Docker build using `--build-arg`. The Dockerfile has been updated to accept these build arguments.

### 3.2 Create Docker Network

```bash
docker network create news-network
```

### 3.3 Run Backend Container

```bash
docker run -d \
  --name news-4u-backend \
  -p 127.0.0.1:8000:8000 \
  -v $(pwd)/backend:/app \
  -v $(pwd)/backend/news_4u.db:/app/news_4u.db \
  --env-file backend/.env \
  --restart unless-stopped \
  news-4u-backend
```

### 3.4 Run Frontend Container

```bash
docker run -d \
  --name news-4u-frontend \
  --network news-network \
  -p 127.0.0.1:3000:3000 \
  -e NEXT_PUBLIC_API_URL=/api \
  -e NEXT_PUBLIC_BASE_PATH=/news \
  --restart unless-stopped \
  news-4u-frontend
```

**Note:** Both services are bound to `127.0.0.1` (localhost only) since nginx will be the public-facing service.

## Step 4: Configure Nginx

### 4.1 Create Nginx Configuration

**Option 1: Copy the provided config file (Recommended)**

```bash
sudo cp ~/news-4u/nginx.conf /etc/nginx/sites-available/news-4u
```

**Option 2: Create manually**

Create a new nginx configuration file:

```bash
sudo nano /etc/nginx/sites-available/news-4u
```

Paste the following configuration (same as `nginx.conf` in project root):

```nginx
server {
    listen 80;
    server_name _;  # Replace with your domain name or IP

    # Increase timeouts for long-running requests
    proxy_read_timeout 300s;
    proxy_connect_timeout 75s;

    # Backend API - Proxy /api/* to backend
    # Note: Backend routes are at /api/news/*, so we preserve the /api prefix
    location /api {
        proxy_pass http://127.0.0.1:8000/api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # CORS headers (if needed)
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
        
        if ($request_method = OPTIONS) {
            return 204;
        }
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # CORS headers (if needed)
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
        
        if ($request_method = OPTIONS) {
            return 204;
        }
    }

    # Frontend - Proxy /news/* to frontend
    # Next.js is configured with basePath=/news, so it expects requests at /news
    # We need to preserve the /news path when proxying
    location /news {
        proxy_pass http://127.0.0.1:3000/news;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Handle Next.js routing
        proxy_redirect off;
    }

    # Optional: Redirect root to /news
    location = / {
        return 301 /news;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### 4.2 Enable the Site

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/news-4u /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

## Step 5: Initialize Database

Run the database initialization script:

```bash
docker exec -it news-4u-backend python scripts/init_db.py
```

## Step 6: Local Testing (Without Nginx)

**Important:** If you're testing locally without nginx, you need to understand how the paths work:

### 6.1 Access URLs (Without Nginx)

When running containers directly without nginx:

- **Frontend:** `http://localhost:3000/` (root path, NOT `/news`)
- **Backend API:** `http://localhost:8000/api`
- **API Docs:** `http://localhost:8000/api/docs`

**Important Notes:**
- **With `basePath=/news`:** Next.js serves the app at root `/`, and the basePath is handled internally. This means:
  - Access the app at `http://localhost:3000/` (root path)
  - If you access `http://localhost:3000/news`, Next.js will redirect to `/` (this is expected behavior)
  - All internal routes and assets are automatically prefixed with `/news`
- **For production with nginx:** Nginx proxies `/news/*` to the frontend at root `/`, and Next.js serves correctly because it's built with `basePath=/news`. The redirect doesn't happen in production because nginx handles the path routing.
- `http://localhost:3000/api` will return 404 - the API is on a different port (8000), not on the frontend container.
- **When testing locally:** Always access at `http://localhost:3000/` (root). The redirect from `/news` to `/` is normal Next.js behavior with basePath.

### 6.2 Common Issues When Testing Locally

**Problem:** Accessing `http://localhost:3000/api` gives 404 errors

**Solution:** 
- The frontend is on port 3000, backend is on port 8000
- Access frontend at: `http://localhost:3000/` (root path, NOT `/news`)
- Access backend at: `http://localhost:8000/api`
- **Note:** If you access `http://localhost:3000/news`, it will redirect to `/` - this is expected Next.js behavior with basePath

**Problem:** Frontend can't reach backend API

**Solution:** 
- The frontend is configured with `NEXT_PUBLIC_API_URL=/api` (relative path) for production with nginx
- For local testing without nginx, you need to rebuild with absolute URL:
  ```bash
  docker build \
    --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 \
    --build-arg NEXT_PUBLIC_BASE_PATH=/news \
    -t news-4u-frontend ./frontend
  ```
  **Note:** Use `http://localhost:8000` (not `/api`) because the API paths already include `/api/news/...`
  
- Then restart the container:
  ```bash
  docker restart news-4u-frontend
  ```

**Problem:** Assets not loading (404 on `/_next/static/...`)

**Solution:**
- Make sure you're accessing the frontend at root path: `http://localhost:3000/` (NOT `/news`)
- With `basePath=/news`, Next.js serves at root `/` and handles the `/news` prefix internally
- Assets will be loaded from `/news/_next/static/...` automatically

### 6.3 Recommended: Use Nginx for Local Testing Too

For the best testing experience that matches production, run nginx locally:

```bash
# Install nginx (if not already installed)
# macOS: brew install nginx
# Linux: sudo apt install nginx

# Copy nginx config
sudo cp ~/news-4u/nginx.conf /etc/nginx/sites-available/news-4u
sudo ln -s /etc/nginx/sites-available/news-4u /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo nginx -s reload

# Now access via nginx:
# Frontend: http://localhost/news
# Backend: http://localhost/api
```

## Step 7: Verify Deployment

### 7.1 Check Services

```bash
# Check Docker containers
docker ps

# Check nginx status
sudo systemctl status nginx

# Check backend logs
docker logs news-4u-backend

# Check frontend logs
docker logs news-4u-frontend
```

### 7.2 Test Endpoints

From your local machine or browser:

```bash
# Health check
curl http://<raspberry-pi-ip>/health

# Backend API
curl http://<raspberry-pi-ip>/api/

# Frontend (should redirect or show page)
curl http://<raspberry-pi-ip>/news
```

### 7.3 Access the Application

- **Frontend:** `http://<raspberry-pi-ip>/news`
- **Backend API:** `http://<raspberry-pi-ip>/api`
- **API Docs:** `http://<raspberry-pi-ip>/api/docs`

## Step 8: Optional - Setup with Docker Compose

Alternatively, you can use Docker Compose. Create a `docker-compose.prod.yml` file:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: news-4u-backend
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./news_4u.db
      - SCHEDULE_ENABLE=true
    volumes:
      - ./backend:/app
      - backend_data:/app/data
    networks:
      - news-network
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        NEXT_PUBLIC_API_URL: /api
        NEXT_PUBLIC_BASE_PATH: /news
    container_name: news-4u-frontend
    ports:
      - "127.0.0.1:3000:3000"
    networks:
      - news-network
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  backend_data:

networks:
  news-network:
    driver: bridge
```

Then run:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Step 9: Setup SSL with Let's Encrypt (Optional)

If you have a domain name, you can set up HTTPS:

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com

# Certbot will automatically update nginx config
# Certificates auto-renew via cron
```

After SSL setup, update the nginx config to redirect HTTP to HTTPS and update the frontend `.env.local` if needed.

## Step 10: Troubleshooting

### Error: "GET http://localhost:3000/api 404" and ChunkLoadError

**Symptoms:**
- Accessing `http://localhost:3000` returns nothing or 404
- Accessing `http://localhost:3000/api` gives 404
- Console shows: `GET http://localhost:3000/api 404 (Not Found)`
- Console shows: `GET http://localhost:3000/news/_next/static/chunks/... 404`
- ChunkLoadError: Loading chunk failed

**Cause:**
- **`http://localhost:3000` returns nothing/404** - This is EXPECTED! The frontend was built with `basePath=/news`, so it only serves content under the `/news` path. Accessing the root (`/`) won't work.
- You're accessing the frontend port (3000) instead of the backend port (8000) for API calls
- The frontend was built with `basePath=/news`, so it must be accessed at `/news` path
- You're trying to access `/api` on the frontend container, which doesn't exist there (API is on port 8000)

**Solution:**
1. **Access the frontend at the correct URL:**
   - Use: `http://localhost:3000/` (root path, NOT `/news` or `/api`)
   - **Note:** If you access `/news`, it will redirect to `/` - this is expected Next.js behavior with basePath

2. **Access the backend separately:**
   - Backend API: `http://localhost:8000/api`
   - API Docs: `http://localhost:8000/api/docs`

3. **For proper routing, use nginx:**
   - With nginx configured, access everything through port 80:
     - Frontend: `http://localhost/news`
     - Backend: `http://localhost/api`

4. **If testing without nginx and frontend can't reach backend:**
   - Rebuild frontend with absolute API URL:
     ```bash
     docker build \
       --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 \
       --build-arg NEXT_PUBLIC_BASE_PATH=/news \
       -t news-4u-frontend ./frontend
     ```
     **Note:** Use `http://localhost:8000` (not `/api` or `http://localhost:8000/api`) because the API paths in the code already include `/api/news/...`
   - Restart the container:
     ```bash
     docker restart news-4u-frontend
     ```

### Backend Not Accessible

1. Check if backend container is running:
   ```bash
   docker ps | grep news-4u-backend
   ```

2. Check backend logs:
   ```bash
   docker logs news-4u-backend
   ```

3. Test backend directly:
   ```bash
   curl http://127.0.0.1:8000/api/
   ```

### Frontend Not Accessible

1. Check if frontend container is running:
   ```bash
   docker ps | grep news-4u-frontend
   ```

2. Check frontend logs:
   ```bash
   docker logs news-4u-frontend
   ```

3. Test frontend directly:
   ```bash
   curl http://127.0.0.1:3000
   ```

### Nginx Issues

1. Check nginx configuration:
   ```bash
   sudo nginx -t
   ```

2. Check nginx error logs:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

3. Check nginx access logs:
   ```bash
   sudo tail -f /var/log/nginx/access.log
   ```

### API Calls Failing

1. Verify `NEXT_PUBLIC_API_URL` is set to `/api` in frontend container:
   ```bash
   docker exec news-4u-frontend env | grep NEXT_PUBLIC_API_URL
   ```

2. Check browser console for CORS errors (shouldn't happen with nginx proxy)

3. Verify nginx is proxying correctly:
   ```bash
   curl -v http://localhost/api/
   ```

### Database Issues

1. Initialize database:
   ```bash
   docker exec -it news-4u-backend python scripts/init_db.py
   ```

2. Check database file permissions:
   ```bash
   ls -la backend/news_4u.db
   ```

### Performance Issues

For better performance on Raspberry Pi:

1. **Reduce memory usage:**
   - Limit Docker container memory if needed
   - Consider using SQLite instead of PostgreSQL for lower resource usage

2. **Optimize Next.js:**
   - The frontend is already configured with `output: 'standalone'` for production

3. **Monitor resources:**
   ```bash
   # Check memory usage
   free -h
   
   # Check CPU usage
   top
   
   # Check Docker resource usage
   docker stats
   ```

## Maintenance

### Update Application

```bash
cd ~/news-4u
git pull

# Rebuild and restart containers
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

### Backup Database

```bash
# Backup SQLite database
cp backend/news_4u.db backend/news_4u.db.backup.$(date +%Y%m%d)
```

### View Logs

```bash
# Backend logs
docker logs -f news-4u-backend

# Frontend logs
docker logs -f news-4u-frontend

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Services

```bash
# Restart backend
docker restart news-4u-backend

# Restart frontend
docker restart news-4u-frontend

# Restart nginx
sudo systemctl restart nginx
```

## Security Considerations

1. **Firewall:** Configure UFW to only allow necessary ports:
   ```bash
   sudo ufw allow 22/tcp  # SSH
   sudo ufw allow 80/tcp  # HTTP
   sudo ufw allow 443/tcp # HTTPS (if using SSL)
   sudo ufw enable
   ```

2. **SSH:** Use key-based authentication and disable password login

3. **Docker:** Keep Docker and containers updated

4. **Nginx:** Regularly update nginx and review security headers

5. **Database:** If using SQLite, ensure proper file permissions

## Network Architecture

```
Internet
   │
   ▼
Nginx (Port 80/443)
   │
   ├── /api/* ──────► Backend (127.0.0.1:8000)
   │
   └── /news/* ─────► Frontend (127.0.0.1:3000)
```

## Summary

After completing these steps, your News 4U application will be:
- ✅ Running on Raspberry Pi 4
- ✅ Backend accessible at `/api`
- ✅ Frontend accessible at `/news`
- ✅ Proxied through Nginx
- ✅ Auto-restarting on reboot
- ✅ Ready for production use

For questions or issues, check the logs and refer to the troubleshooting section above.

