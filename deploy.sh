#!/bin/bash

# ==========================================
# Marka AI - VPS Deploy Script
# ==========================================
# This script deploys Marka AI to VPS using Docker Compose
# Run on your VPS: bash deploy.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}  Marka AI - Deployment Script  ${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Detect docker-compose or docker compose
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Create application directory
APP_DIR="/opt/marka-ai"
echo -e "${YELLOW}Creating application directory: ${APP_DIR}${NC}"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Go to application directory
cd $APP_DIR

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}Git is not installed. Installing...${NC}"
    sudo apt update
    sudo apt install -y git
fi

# Pull latest code
echo -e "${YELLOW}Pulling latest code from GitHub...${NC}"
git pull origin main || {
    echo -e "${RED}Error: Failed to pull code. Make sure you have pushed to main branch first.${NC}"
    exit 1
}

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env <<EOF
POSTGRES_PASSWORD=$(openssl rand -base64 32)
PINECONE_API_KEY=your_pinecone_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
EOF
    echo -e "${GREEN}Created .env file. Please update with your actual API keys.${NC}"
    echo -e "${YELLOW}Your PostgreSQL password is: $(grep POSTGRES_PASSWORD .env | cut -d= -f2)${NC}"
fi

# Create necessary directories
mkdir -p data

# Pull latest images
echo -e "${YELLOW}Pulling latest Docker images...${NC}"
$DOCKER_COMPOSE pull

# Stop old containers
echo -e "${YELLOW}Stopping old containers...${NC}"
$DOCKER_COMPOSE down

# Start new containers
echo -e "${YELLOW}Starting containers...${NC}"
$DOCKER_COMPOSE up -d --build

# Wait for services to be healthy
echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
sleep 10

# Check service health
echo -e "${YELLOW}Checking service health...${NC}"
for service in backend frontend ai postgres redis; do
    if $DOCKER_COMPOSE ps $service | grep -q "healthy"; then
        echo -e "${GREEN}✓ $service is healthy${NC}"
    else
        echo -e "${RED}✗ $service is NOT healthy${NC}"
    fi
done

# Show logs
echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}  Deployment Complete!  ${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  View logs: $DOCKER_COMPOSE logs -f"
echo "  Check status: $DOCKER_COMPOSE ps"
echo "  Restart services: $DOCKER_COMPOSE restart"
echo "  Stop all: $DOCKER_COMPOSE down"
echo ""

# Show service URLs
echo -e "${YELLOW}Service URLs:${NC}"
echo "  Frontend: http://$(curl -s ifconfig.me):5173"
echo "  Backend API: http://$(curl -s ifconfig.me):3000"
echo "  AI Backend: http://$(curl -s ifconfig.me):8000"
echo "  PostgreSQL: $(curl -s ifconfig.me):5432"
echo "  Redis: $(curl -s ifconfig.me):6379"
echo ""

exit 0
