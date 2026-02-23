# Linode Deployment Guide for News 4U

This guide walks you through deploying the News 4U application on Linode using Docker containers with PostgreSQL 17.

## Prerequisites

- A Linode account
- A Linode instance (Ubuntu 22.04 or later recommended)
- Domain name (optional, but recommended)
- Basic knowledge of Linux and SSH

## 1. Create a Linode Instance

1. Log in to your Linode account at [cloud.linode.com](https://cloud.linode.com)
2. Click "Create Linode"
3. Choose:
   - **Distribution**: Ubuntu 22.04 LTS
   - **Region**: Select closest to your target audience
   - **Plan**: Minimum 4GB RAM (Dedicated 4GB or Shared 4GB)
   - **Label**: news-4u-production
4. Set a strong root password
5. Add your SSH key (recommended)
6. Click "Create Linode"

## 2. Initial Server Setup

SSH into your server:

```bash
ssh root@your-linode-ip
```

### Update System

```bash
apt update && apt upgrade -y
```

### Create a Non-Root User

```bash
adduser news4u
usermod -aG sudo news4u
```

### Configure Firewall

```bash
# Install UFW (if not already installed)
apt install ufw -y

# Allow SSH, HTTP, and HTTPS
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp  # Backend API
ufw allow 3000/tcp  # Frontend (optional, can be behind reverse proxy)

# Enable firewall
ufw enable
```

## 3. Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add your user to docker group
usermod -aG docker news4u

# Install Docker Compose (standalone)
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify installations
docker --version
docker-compose --version
```

## 4. Deploy Your Application

### Switch to Application User

```bash
su - news4u
```

### Clone or Upload Your Application

Option A - Using Git:
```bash
git clone https://github.com/your-username/news-4u.git
cd news-4u
```

Option B - Upload files via SCP (from your local machine):
```bash
scp -r /path/to/news-4u news4u@your-linode-ip:/home/news4u/
```

### Configure Environment Variables

```bash
cd news-4u
cp .env.example .env
nano .env
```

Update the following in your `.env` file:

```env
# Database Configuration (CHANGE THESE!)
DB_NAME=news_4u
DB_USER=postgres
DB_PASS=SECURE_PASSWORD_HERE  # Use a strong password!
DB_HOST=postgres
DB_PORT=5432

# Application Configuration
SCHEDULE_ENABLE=true
ARTICLE_EXTRACTION_MAX_RETRY=3
LOG_LEVEL=INFO
APP_ENV=production
SECRET_KEY=GENERATE_SECURE_KEY_HERE  # Use: openssl rand -hex 32

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Port Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000

# Frontend Configuration
# IMPORTANT: Update with your domain or server IP
NEXT_PUBLIC_API_URL=http://your-domain.com:8000
# OR
NEXT_PUBLIC_API_URL=http://YOUR_LINODE_IP:8000
```

Generate a secure secret key:
```bash
openssl rand -hex 32
```

### Build and Start Services

For production deployment:

```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Check container status
docker-compose -f docker-compose.prod.yml ps
```

For development deployment:

```bash
docker-compose up -d --build
```

### Verify Deployment

```bash
# Check if containers are running
docker ps

# Test backend health
curl http://localhost:8000/api/news/health

# Test frontend
curl http://localhost:3000
```

## 5. Set Up Reverse Proxy (Recommended)

### Install Nginx

```bash
sudo apt install nginx -y
```

### Configure Nginx

Create a new Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/news4u
```

Add the following configuration:

```nginx
# Frontend
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Backend API
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/news4u /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Set Up SSL with Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com -d api.your-domain.com

# Certbot will automatically configure SSL and set up auto-renewal
```

Update your `.env` file to use HTTPS:
```env
NEXT_PUBLIC_API_URL=https://api.your-domain.com
```

Restart containers:
```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

## 6. Database Backup Setup

Create a backup script:

```bash
nano ~/backup-db.sh
```

Add the following:

```bash
#!/bin/bash
BACKUP_DIR="/home/news4u/backups"
DATE=$(date +%Y%m%d_%H%M%S)
CONTAINER_NAME="news4u-postgres"

mkdir -p $BACKUP_DIR

docker exec $CONTAINER_NAME pg_dump -U postgres news_4u > $BACKUP_DIR/news4u_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "news4u_*.sql" -mtime +7 -delete

echo "Backup completed: news4u_$DATE.sql"
```

Make it executable:

```bash
chmod +x ~/backup-db.sh
```

Set up daily backups with cron:

```bash
crontab -e
```

Add this line for daily backups at 2 AM:

```cron
0 2 * * * /home/news4u/backup-db.sh >> /home/news4u/backup.log 2>&1
```

## 7. Monitoring and Maintenance

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
docker-compose -f docker-compose.prod.yml logs -f postgres
```

### Restart Services

```bash
# Restart all
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend
```

### Update Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build
```

### Check System Resources

```bash
# Container stats
docker stats

# Disk usage
docker system df

# System resources
htop  # or top
```

## 8. Troubleshooting

### Containers Not Starting

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check container status
docker ps -a

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose -f docker-compose.prod.yml ps postgres

# Connect to database manually
docker exec -it news4u-postgres psql -U postgres -d news_4u

# View database logs
docker-compose -f docker-compose.prod.yml logs postgres
```

### Port Already in Use

```bash
# Find what's using the port
sudo lsof -i :8000
sudo lsof -i :3000

# Kill the process
sudo kill -9 <PID>
```

### Out of Disk Space

```bash
# Clean up Docker
docker system prune -a --volumes

# Check disk usage
df -h
du -sh /home/news4u/*
```

### Frontend Can't Connect to Backend

1. Check `NEXT_PUBLIC_API_URL` in `.env`
2. Verify CORS settings in [backend/main.py](backend/main.py:51-64)
3. Check firewall rules: `sudo ufw status`
4. Test backend directly: `curl http://localhost:8000/api/news/health`

## 9. Security Best Practices

1. **Keep System Updated**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Use Strong Passwords**
   - Change default PostgreSQL password
   - Use strong `SECRET_KEY`

3. **Enable Firewall**
   - Only expose necessary ports
   - Consider closing direct database access (port 5432)

4. **Regular Backups**
   - Set up automated database backups
   - Test restore procedures

5. **Monitor Logs**
   - Regularly check application and system logs
   - Set up alerting for critical errors

6. **SSL/TLS**
   - Always use HTTPS in production
   - Keep SSL certificates up to date

7. **Environment Variables**
   - Never commit `.env` file to version control
   - Use secure values for production

## 10. Scaling Considerations

### Increase Resources

If your application needs more resources:

1. Go to Linode Dashboard
2. Select your Linode
3. Click "Resize"
4. Choose a larger plan
5. Reboot instance

### Database Performance

For better database performance:

```yaml
# In docker-compose.prod.yml, add to postgres service:
command:
  - postgres
  - -c
  - shared_buffers=256MB
  - -c
  - max_connections=200
  - -c
  - work_mem=4MB
```

### Add Redis for Caching (Optional)

Add to [docker-compose.prod.yml](docker-compose.prod.yml):

```yaml
redis:
  image: redis:7-alpine
  container_name: news4u-redis
  restart: always
  networks:
    - news-network
  volumes:
    - redis_data:/data
```

## Support

For issues specific to this application, see:
- [README.md](README.md)
- [DOCUMENTATION.md](DOCUMENTATION.md)
- [backend/README.md](backend/README.md)

For Linode-specific issues:
- [Linode Documentation](https://www.linode.com/docs/)
- [Linode Community](https://www.linode.com/community/questions/)
