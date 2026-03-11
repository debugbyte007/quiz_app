# Deploy Quiz App to Render using CLI (PowerShell version)
# Make sure you have Render CLI installed and authenticated

param(
    [string]$Region = "oregon",
    [string]$Plan = "starter"
)

Write-Host "🚀 Deploying Quiz App to Render using CLI..." -ForegroundColor Green

# Check if Render CLI is installed
try {
    render --version | Out-Null
    Write-Host "✅ Render CLI found!" -ForegroundColor Green
} catch {
    Write-Host "❌ Render CLI not found!" -ForegroundColor Red
    Write-Host "Install it with:" -ForegroundColor Yellow
    Write-Host "npm install -g @render/cli"
    Write-Host "# or download from: https://cli.render.com/"
    exit 1
}

# Check if user is authenticated
Write-Host "🔐 Checking authentication..." -ForegroundColor Blue
try {
    render services --output text | Out-Null
    Write-Host "✅ Render CLI authenticated!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Not authenticated. Please run:" -ForegroundColor Yellow
    Write-Host "render login"
    exit 1
}

# Check if render.yaml exists, if not create it
if (-not (Test-Path "render.yaml")) {
    Write-Host "📝 Creating render.yaml blueprint..." -ForegroundColor Yellow
    
    $renderYaml = @"
services:
  - type: web
    name: quiz-app-backend
    runtime: python3
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && gunicorn --config gunicorn.conf.py app:app
    plan: $Plan
    region: $Region
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
    region: $Region
    branch: main
    routes:
      - type: rewrite
        source: /api/*
        destination: https://quiz-app-backend.onrender.com/api/*
"@
    
    $renderYaml | Out-File -FilePath "render.yaml" -Encoding UTF8
    Write-Host "✅ Created render.yaml" -ForegroundColor Green
}

# Validate the blueprint
Write-Host "🔍 Validating render.yaml..." -ForegroundColor Blue
try {
    render blueprints validate render.yaml
    Write-Host "✅ Blueprint is valid!" -ForegroundColor Green
} catch {
    Write-Host "❌ Blueprint validation failed!" -ForegroundColor Red
    exit 1
}

# Deploy using blueprint
Write-Host "🚀 Deploying to Render..." -ForegroundColor Blue
Write-Host "Note: You'll need to set SUPABASE_URL and SUPABASE_KEY manually in the Render dashboard" -ForegroundColor Yellow

Write-Host "`n📦 To deploy, run:" -ForegroundColor Blue
Write-Host "render blueprints launch render.yaml" -ForegroundColor Cyan

Write-Host "`n🔄 Alternative: Deploy existing services" -ForegroundColor Blue
Write-Host "If you already have services created:" -ForegroundColor Yellow
Write-Host "1. render services" -ForegroundColor Cyan
Write-Host "2. Select your service and choose 'Deploy'" -ForegroundColor Cyan

Write-Host "`n🎉 Deployment configuration ready!" -ForegroundColor Green
Write-Host "📊 After deployment:" -ForegroundColor Blue
Write-Host "1. Set environment variables in Render dashboard" -ForegroundColor Yellow
Write-Host "2. Update frontend/api.js with your backend URL" -ForegroundColor Yellow
Write-Host "3. Test your deployed app!" -ForegroundColor Yellow

# Optionally launch the blueprint
$launch = Read-Host "`nDo you want to launch the blueprint now? (y/N)"
if ($launch -eq "y" -or $launch -eq "Y") {
    Write-Host "🚀 Launching blueprint..." -ForegroundColor Green
    render blueprints launch render.yaml
}