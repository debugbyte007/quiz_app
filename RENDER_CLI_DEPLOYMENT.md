# 🚀 Render CLI Deployment Guide

## Quick Deploy Options

| Method | Difficulty | Time | Best For |
|--------|------------|------|----------|
| **Render CLI** | Easy | 5 min | Developers who love CLI |
| **GitHub Integration** | Easiest | 3 min | Auto-deploy on push |
| **Blueprint (render.yaml)** | Easy | 5 min | Infrastructure as Code |

---

## 🛠 Option 1: Render CLI Deployment

### Step 1: Install Render CLI

**Windows (PowerShell):**
```powershell
# Using npm (if you have Node.js)
npm install -g @render/cli

# Or download directly
Invoke-WebRequest -Uri "https://cli.render.com/install.ps1" -OutFile "install.ps1"
.\install.ps1
```

**macOS/Linux:**
```bash
# Using npm
npm install -g @render/cli

# Or using curl
curl -fsSL https://cli.render.com/install | sh

# Or using Homebrew (macOS)
brew install render
```

### Step 2: Authenticate

```bash
render login
```

This opens your browser to authenticate and generates a CLI token.

### Step 3: Deploy Using Our Scripts

**Linux/macOS:**
```bash
chmod +x deploy-render-cli.sh
./deploy-render-cli.sh
```

**Windows:**
```powershell
.\deploy-render-cli.ps1
```

### Step 4: Deploy Existing Services (if you have service IDs)

```bash
# Deploy backend
render deploys create srv-your-backend-id --wait

# Deploy frontend  
render deploys create srv-your-frontend-id --wait
```

---

## 📋 Option 2: Blueprint Deployment (render.yaml)

### What is a Blueprint?
A `render.yaml` file that defines your entire infrastructure as code.

### Step 1: Use Our Blueprint

We've already created `render.yaml` for you! It includes:
- ✅ Backend web service (Python/Flask)
- ✅ Frontend static site
- ✅ Environment variables
- ✅ Health checks
- ✅ Auto-scaling configuration

### Step 2: Deploy via Dashboard

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New" → "Blueprint"**
3. **Connect GitHub repository**: `debugbyte007/quiz_app`
4. **Render automatically detects `render.yaml`**
5. **Click "Apply"**
6. **Set environment variables:**
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase anon key

### Step 3: Validate Blueprint (Optional)

```bash
render blueprints validate render.yaml
```

---

## 🔄 Option 3: GitHub Auto-Deploy

### Step 1: Connect Repository

1. **Go to Render Dashboard**
2. **Click "New" → "Web Service"**
3. **Connect GitHub**: `debugbyte007/quiz_app`
4. **Configure:**
   ```
   Name: quiz-app-backend
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --config gunicorn.conf.py app:app
   ```

### Step 2: Auto-Deploy Setup

Render automatically deploys when you push to `main` branch!

```bash
git add .
git commit -m "Update app"
git push origin main
# 🚀 Auto-deploys to Render!
```

---

## 🎯 CLI Commands Cheat Sheet

### Authentication
```bash
render login                    # Authenticate
render logout                   # Logout
```

### Services Management
```bash
render services                 # List all services
render services --output json  # JSON format
render ssh srv-xxxxx           # SSH into service
```

### Deployments
```bash
render deploys list srv-xxxxx           # List deploys
render deploys create srv-xxxxx         # Trigger deploy
render deploys create srv-xxxxx --wait  # Wait for completion
```

### Logs
```bash
render logs srv-xxxxx           # View logs
render logs srv-xxxxx --tail    # Follow logs
```

### Environment Variables
```bash
render env srv-xxxxx            # List env vars
render env set srv-xxxxx KEY=value  # Set env var
```

### Databases
```bash
render psql db-xxxxx           # Connect to PostgreSQL
render psql db-xxxxx -c "SELECT * FROM users;"  # Run query
```

---

## 🔧 Advanced CLI Usage

### Non-Interactive Mode (for CI/CD)

```bash
# Set API key for automation
export RENDER_API_KEY=your-api-key

# Deploy with confirmation skip
render deploys create srv-xxxxx --confirm --wait --output json
```

### GitHub Actions Integration

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Render CLI
        run: npm install -g @render/cli
        
      - name: Deploy Backend
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: render deploys create ${{ secrets.RENDER_SERVICE_ID }} --wait
```

### Bulk Operations

```bash
# Deploy multiple services
for service in srv-backend srv-frontend; do
  render deploys create $service --wait
done

# Check status of all services
render services --output json | jq '.[] | {name: .name, status: .status}'
```

---

## 🚨 Troubleshooting

### CLI Not Found
```bash
# Check installation
which render
render --version

# Reinstall if needed
npm uninstall -g @render/cli
npm install -g @render/cli
```

### Authentication Issues
```bash
# Clear and re-authenticate
render logout
render login

# Or use API key
export RENDER_API_KEY=your-key
```

### Service Not Found
```bash
# List all services to find correct ID
render services --output text

# Check workspace
render workspace set
```

### Deploy Failures
```bash
# Check logs
render logs srv-xxxxx --tail

# Check deploy status
render deploys list srv-xxxxx
```

---

## 📊 Deployment Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **CLI** | Fast, scriptable, powerful | Requires setup | Developers |
| **Dashboard** | Visual, easy, no setup | Manual process | Beginners |
| **Blueprint** | Infrastructure as Code | Initial setup | Teams |
| **GitHub** | Auto-deploy, simple | Less control | Continuous deployment |

---

## 🎉 Quick Start Commands

```bash
# 1. Install CLI
npm install -g @render/cli

# 2. Login
render login

# 3. Deploy (if services exist)
render deploys create srv-your-backend-id --wait
render deploys create srv-your-frontend-id --wait

# 4. Check status
render services

# 5. View logs
render logs srv-your-backend-id --tail
```

---

## 💡 Pro Tips

1. **Save Service IDs**: Store them in environment variables
   ```bash
   export BACKEND_SERVICE_ID=srv-xxxxx
   export FRONTEND_SERVICE_ID=srv-yyyyy
   ```

2. **Use Aliases**: Create shortcuts for common commands
   ```bash
   alias rdeploy="render deploys create $BACKEND_SERVICE_ID --wait"
   alias rlogs="render logs $BACKEND_SERVICE_ID --tail"
   ```

3. **Monitor Deployments**: Use `--wait` flag to block until completion

4. **JSON Output**: Use `--output json` for scripting and automation

5. **Health Checks**: Monitor service health with CLI
   ```bash
   render services --output json | jq '.[] | select(.status != "available")'
   ```

Your quiz app is now ready for CLI-based deployment! 🚀