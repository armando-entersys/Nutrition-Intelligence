#!/bin/bash
# Deployment script for Nutrition Intelligence to Google Cloud VM

set -e

echo "🚀 Deploying Nutrition Intelligence to Production"
echo "================================================="

# Configuration
VM_NAME="prod-server"
VM_ZONE="us-central1-c"
PROJECT_ID="mi-infraestructura-web"
DEPLOY_DIR="/srv/scram-apps/nutrition-intelligence"
REPO_URL="https://github.com/armando-entersys/Nutrition-Intelligence.git"

# Colors for output
GREEN='\033[0.32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Connecting to VM...${NC}"
echo "VM: $VM_NAME ($VM_ZONE)"
echo ""

# Execute deployment commands on the VM
gcloud compute ssh $VM_NAME \
  --zone=$VM_ZONE \
  --project=$PROJECT_ID \
  --command="
    set -e
    echo '📦 Setting up deployment directory...'
    sudo mkdir -p $DEPLOY_DIR
    sudo chown -R \$USER:www-data $DEPLOY_DIR
    
    if [ -d $DEPLOY_DIR/.git ]; then
      echo '🔄 Updating existing repository...'
      cd $DEPLOY_DIR
      git pull origin main
    else
      echo '📥 Cloning repository...'
      git clone $REPO_URL $DEPLOY_DIR
      cd $DEPLOY_DIR
    fi
    
    echo '🔑 Setting up production environment variables...'
    if [ ! -f backend/.env ]; then
      cp backend/.env.example backend/.env
      echo 'Please configure backend/.env with your production credentials'
    fi
    
    echo '🐳 Building and starting Docker containers...'
    docker-compose down || true
    docker-compose build
    docker-compose up -d
    
    echo '⏳ Waiting for services to start...'
    sleep 10
    
    echo '✅ Checking service health...'
    docker-compose ps
    
    echo ''
    echo '🎉 Deployment completed!'
    echo '📍 Your application should be available at:'
    echo '   http://nutrition-intelligence.scram2k.com'
    echo ''
    echo '📊 To view logs:'
    echo '   docker-compose logs -f'
  "

echo -e "${GREEN}✨ Deployment process finished!${NC}"
echo ""
echo "Next steps:"
echo "1. SSH into the server and configure backend/.env with your credentials"
echo "2. Update DNS to point nutrition-intelligence.scram2k.com to 34.59.193.54"
echo "3. Verify the application is running: http://nutrition-intelligence.scram2k.com"

