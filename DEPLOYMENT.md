# Marka AI - CI/CD & Deployment Guide

This guide explains how to set up and use the CI/CD pipeline with Docker deployment to your VPS.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [GitHub Repository Setup](#github-repository-setup)
3. [VPS Preparation](#vps-preparation)
4. [GitHub Secrets Configuration](#github-secrets-configuration)
5. [Local Development](#local-development)
6. [CI/CD Pipeline Flow](#cicd-pipeline-flow)
7. [Deployment Process](#deployment-process)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### GitHub Repository
- GitHub account
- Repository created (public or private)
- Code pushed to `main` branch

### VPS Requirements
- 2 CPU cores (you have exactly this)
- 2GB RAM (exact match - no wiggle room)
- 10GB disk space
- Linux operating system (Ubuntu 20.04+ recommended)
- Root or sudo access

### Services Required on VPS
- Docker (20.10+)
- Docker Compose (2.0+)

---

## GitHub Repository Setup

### 1. Create Repository on GitHub
```bash
# Create new repository on GitHub website
# Make it private if you want

# Clone locally
git clone https://github.com/YOUR_USERNAME/marka-ai.git
cd marka-ai
```

### 2. Add .gitignore
The `.gitignore` file is already created to exclude:
- `.env` files (secrets)
- `node_modules/` (dependencies)
- `__pycache__/` (Python cache)
- `dist/` (compiled files)
- IDE files (`.vscode`, `.idea`)

### 3. Commit and Push
```bash
git add .
git commit -m "Initial commit: CI/CD setup with Docker"
git push origin main
```

---

## VPS Preparation

### 1. Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add current user to docker group
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
# Or run: newgrp docker
```

### 3. Install Docker Compose
```bash
sudo apt install -y docker-compose-plugin
```

### 4. Verify Installation
```bash
docker --version      # Should show Docker version 25.0+
docker compose version # Should show Compose version 2.20+
```

### 5. Create Application Directory
```bash
sudo mkdir -p /opt/marka-ai
sudo chown $USER:$USER /opt/marka-ai
cd /opt/marka-ai
```

---

## GitHub Secrets Configuration

You need to add 3 secrets to your GitHub repository:

### Step 1: Generate SSH Key Pair
```bash
# Generate SSH key for GitHub Actions
ssh-keygen -t rsa -b 4096 -C "github-actions@marka-ai" -f ~/.ssh/github_actions_deploy

# View private key (copy this to GitHub Secrets)
cat ~/.ssh/github_actions_deploy

# View public key (add this to VPS SSH authorized_keys)
cat ~/.ssh/github_actions_deploy.pub
```

### Step 2: Add Private Key to GitHub Secrets
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `GITHUB_ACTIONS_DEPLOY_KEY`
5. Value: Paste the private key content
6. Click "Add secret"

### Step 3: Add VPS Details to GitHub Secrets
1. Click "New repository secret"
2. Name: `VPS_HOST`
3. Value: Your VPS IP address or hostname
4. Click "Add secret"

5. Click "New repository secret"
6. Name: `VPS_USER`
7. Value: Your SSH username (usually ubuntu, root, or your username)
8. Click "Add secret"

---

## Local Development

### Windows with Docker Desktop

**IMPORTANT**: On Windows, always run Docker Compose from WSL2 to avoid build context and path issues.

```powershell
# Open WSL2
wsl

# Navigate to project in WSL
cd /mnt/d/AHMED_DATA/Projects/marka_ai

# Start all services
docker compose up -d
```

Or from PowerShell in one command:
```powershell
wsl -d Ubuntu -- cd /mnt/d/AHMED_DATA/Projects/marka_ai && docker compose up -d
```

### Linux / macOS

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/marka-ai.git
cd marka-ai
```

### 2. Create .env File
```bash
cp .env.example .env
# Edit .env with your actual values:
nano .env
```

**Note**: A `.env` file is now included in the project. Docker Compose will automatically load it from the root directory.

### 3. Start All Services
```bash
docker compose up -d
```

### 4. Check Services
```bash
docker compose ps
docker compose logs -f
```

### 5. Access Services
| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:3000/health |
| AI Backend | http://localhost:8001/health |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6380 |

**Note**: These are host ports. Internally (in Docker network), services use different ports:
- Frontend container: port 3000
- AI Backend container: port 8000
- Redis container: port 6379

---

## CI/CD Pipeline Flow

### When You Push to Main Branch:
1. **Trigger**: GitHub Actions workflow starts
2. **CI Jobs Run** (in parallel):
   - Backend: Lint → Test → Build
   - Frontend: Lint → Test → Build
   - AI Backend: Lint → Test → Build
3. **Build Docker Images**:
   - Backend image → Push to GHCR
   - Frontend image → Push to GHCR
   - AI image → Push to GHCR
4. **Deploy to VPS** (if main branch):
   - SSH into VPS
   - Pull latest code
   - Pull new Docker images
   - Restart containers with new images

### When You Create a Pull Request:
1. CI runs only (no deployment)
2. Checks all services pass
3. Merge to main → deployment runs automatically

---

## Deployment Process

### Manual Deployment (Optional)
If you don't want automatic deployment:

```bash
# On VPS
cd /opt/marka-ai
bash deploy.sh
```

### Automatic Deployment
Just push to main branch:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

### View Deployment Status
- GitHub Actions tab → Select workflow → View runs
- VPS: `docker compose ps`

### Rollback
```bash
# On VPS
cd /opt/marka-ai
git log --oneline -5
# Find commit hash you want to revert to
git reset --hard <commit-hash>
docker compose up -d --build
```

---

## Troubleshooting

### Common Issues

#### 1. "SSH: Connection refused"
```bash
# Check SSH service is running
sudo systemctl status ssh

# Check firewall
sudo ufw status

# Allow SSH
sudo ufw allow 22/tcp
```

#### 2. "Permission denied (publickey)"
```bash
# Add public key to VPS
sudo bash -c 'cat ~/.ssh/github_actions_deploy.pub >> /home/$VPS_USER/.ssh/authorized_keys'
sudo chmod 600 /home/$VPS_USER/.ssh/authorized_keys
sudo chmod 700 /home/$VPS_USER/.ssh
```

#### 3. Docker images not found
```bash
# Pull images manually
cd /opt/marka-ai
docker compose pull
```

#### 4. Out of memory errors
```bash
# Check available memory
free -h

# Reduce services running
docker compose down
# Or comment out non-essential services in docker-compose.yml
```

#### 5. Port already in use
```bash
# Check what's using the port
sudo lsof -i :3000
# Kill the process or change ports in docker-compose.yml
```

### Getting Logs
```bash
# View all service logs
docker compose logs -f

# View specific service
docker compose logs -f backend
docker compose logs -f ai

# View last 100 lines
docker compose logs --tail=100
```

### Restart Services
```bash
docker compose restart
docker compose restart backend
```

### Stop All Services
```bash
docker compose down
docker compose down -v  # Also remove volumes
```

---

## Monitoring

### Health Checks
All services have health checks:
- Backend: http://localhost:3000/health
- Frontend: http://localhost:5173
- AI Backend: http://localhost:8001/health
- PostgreSQL: Database connection
- Redis: PING command

### Resource Usage
```bash
# Check container stats
docker stats

# Check Docker disk usage
docker system df
```

---

## Maintenance

### Update Application
```bash
# On VPS
cd /opt/marka-ai
git pull
docker compose pull
docker compose up -d
```

### Backup Database
```bash
# Backup PostgreSQL
docker exec marka-postgres pg_dump -U marka_user marka_db > backup.sql
```

### Restore Database
```bash
# Restore PostgreSQL
docker exec -i marka-postgres psql -U marka_user marka_db < backup.sql
```

---

## Summary

✅ **CI/CD benefits**:
- Automated testing on every push
- Docker containers for consistency
- Automatic deployment to VPS
- Built-in rollback capability
- Free tier on GitHub (public repos)

✅ **Next steps**:
1. Create GitHub repository
2. Set up VPS with Docker
3. Add GitHub Secrets
4. Test deployment
5. Start developing!

---

For more help, check main [README.md](../README.md) or [AGENTS.md](../AGENTS.md).
