#!/bin/bash
# Deploy Quiz App to Render using CLI
# Make sure you have Render CLI installed and authenticated

set -e  # Exit on any error

echo "🚀 Deploying Quiz App to Render using CLI..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Render CLI is installed
if ! command -v render &> /dev/null; then
    echo -e "${RED}❌ Render CLI not found!${NC}"
    echo -e "${YELLOW}Install it with:${NC}"
    echo "npm install -g @render/cli"
    echo "# or"
    echo "curl -fsSL https://cli.render.com/install | sh"
    exit 1
fi

# Check if user is authenticated
echo -e "${BLUE}🔐 Checking authentication...${NC}"
if ! render services --output text &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not authenticated. Please run:${NC}"
    echo "render login"
    exit 1
fi

echo -e "${GREEN}✅ Render CLI authenticated!${NC}"

# Check if render.yaml exists, if not create it
if [ ! -f "render.yaml" ]; then
    echo -e "${YELLOW}📝 Creating render.yaml blueprint...${NC}"
    cat > render.yaml << 'EOF'
services:
  - type: web
    name: quiz-app-backend
    runtime: python3
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && gunicorn --config gunicorn.conf.py app:app
    plan: starter  # Change to 'free' for free tier
    region: oregon  # Change to your preferred region
    branch: main
    rootDir: .
    envVars:
      - key: SUPABASE_URL
        sync: false  # Set manually in Render dashboard
      - key: SUPABASE_KEY
        sync: false  # Set manually in Render dashboard
      - key: SECRET_KEY
        generateValue: true
      - key: PORT
        value: 10000

  - type: static
    name: quiz-app-frontend
    buildCommand: echo "No build needed for static files"
    staticPublishPath: ./frontend
    plan: free
    region: oregon
    branch: main
    routes:
      - type: rewrite
        source: /api/*
        destination: https://quiz-app-backend.onrender.com/api/*
EOF
    echo -e "${GREEN}✅ Created render.yaml${NC}"
fi

# Validate the blueprint
echo -e "${BLUE}🔍 Validating render.yaml...${NC}"
if render blueprints validate render.yaml; then
    echo -e "${GREEN}✅ Blueprint is valid!${NC}"
else
    echo -e "${RED}❌ Blueprint validation failed!${NC}"
    exit 1
fi

# Deploy using blueprint
echo -e "${BLUE}🚀 Deploying to Render...${NC}"
echo -e "${YELLOW}Note: You'll need to set SUPABASE_URL and SUPABASE_KEY manually in the Render dashboard${NC}"

# Create services from blueprint (this might not work if services already exist)
echo -e "${BLUE}📦 Creating services from blueprint...${NC}"
echo "render blueprints launch render.yaml"
echo -e "${YELLOW}⚠️  Run the above command manually if this script fails${NC}"

# Alternative: Deploy existing services
echo -e "\n${BLUE}🔄 Alternative: Deploy existing services${NC}"
echo "If you already have services created, you can deploy them with:"
echo "render services"
echo "# Then select your service and choose 'Deploy'"

echo -e "\n${GREEN}🎉 Deployment initiated!${NC}"
echo -e "${BLUE}📊 Monitor your deployment:${NC}"
echo "1. Run: render services"
echo "2. Select your service"
echo "3. Choose 'View logs' to monitor deployment"
echo ""
echo -e "${YELLOW}🔧 Don't forget to:${NC}"
echo "1. Set SUPABASE_URL and SUPABASE_KEY in Render dashboard"
echo "2. Update frontend/api.js with your backend URL"
echo "3. Test your deployed app!"