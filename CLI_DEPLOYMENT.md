# 🚀 CLI Deployment Options for Quiz App

## ✅ Render CLI (Official) - INSTALLED!

### Installation ✅ DONE
The Render CLI is now installed and ready to use!

### Quick Start
```bash
# 1. Authenticate (opens browser)
render login

# 2. Set workspace
render workspace set

# 3. Validate our blueprint
render blueprints validate render.yaml

# 4. Deploy!
render blueprints launch render.yaml
```

### Available Commands
```bash
render services          # List all services
render deploys create    # Trigger deployment
render logs             # View service logs
render ssh              # SSH into service
render --help           # Full command list
```

---

## Railway CLI

### Installation
```bash
npm install -g @railway/cli
# or
curl -fsSL https://railway.app/install.sh | sh
```

### Deploy
```bash
# 1. Login
railway login

# 2. Initialize project
railway init

# 3. Deploy
railway up

# 4. Set environment variables
railway variables set SUPABASE_URL=your-url
railway variables set SUPABASE_KEY=your-key
railway variables set SECRET_KEY=your-secret
```

---

## Vercel CLI

### Installation
```bash
npm install -g vercel
```

### Deploy Frontend Only
```bash
# 1. Login
vercel login

# 2. Deploy frontend
cd frontend
vercel

# 3. Set environment variables
vercel env add VITE_API_BASE
# Enter: https://your-backend-url.onrender.com/api
```

---

## Netlify CLI

### Installation
```bash
npm install -g netlify-cli
```

### Deploy Frontend Only
```bash
# 1. Login
netlify login

# 2. Deploy
cd frontend
netlify deploy

# 3. Production deploy
netlify deploy --prod
```

---

## DigitalOcean App Platform CLI

### Installation
```bash
# Install doctl
curl -sL https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-linux-amd64.tar.gz | tar -xzv
sudo mv doctl /usr/local/bin
```

### Deploy
```bash
# 1. Authenticate
doctl auth init

# 2. Create app spec
cat > .do/app.yaml << EOF
name: quiz-app
services:
- name: backend
  source_dir: /backend
  github:
    repo: debugbyte007/quiz_app
    branch: main
  run_command: gunicorn --config gunicorn.conf.py app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: SUPABASE_URL
    value: your-url
  - key: SUPABASE_KEY
    value: your-key
- name: frontend
  source_dir: /frontend
  github:
    repo: debugbyte007/quiz_app
    branch: main
  static_sites:
  - name: frontend
    source_dir: /frontend
EOF

# 3. Deploy
doctl apps create .do/app.yaml
```

---

## Heroku CLI

### Installation
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh
```

### Deploy
```bash
# 1. Login
heroku login

# 2. Create apps
heroku create quiz-app-backend
heroku create quiz-app-frontend

# 3. Deploy backend
git subtree push --prefix backend heroku main

# 4. Set environment variables
heroku config:set SUPABASE_URL=your-url -a quiz-app-backend
heroku config:set SUPABASE_KEY=your-key -a quiz-app-backend
heroku config:set SECRET_KEY=your-secret -a quiz-app-backend
```

---

## AWS CLI (Elastic Beanstalk)

### Installation
```bash
pip install awscli awsebcli
```

### Deploy
```bash
# 1. Configure AWS
aws configure

# 2. Initialize EB
cd backend
eb init quiz-app --platform python-3.9

# 3. Create environment
eb create production

# 4. Deploy
eb deploy

# 5. Set environment variables
eb setenv SUPABASE_URL=your-url SUPABASE_KEY=your-key SECRET_KEY=your-secret
```

---

## Google Cloud CLI

### Installation
```bash
curl https://sdk.cloud.google.com | bash
```

### Deploy to Cloud Run
```bash
# 1. Login
gcloud auth login

# 2. Set project
gcloud config set project your-project-id

# 3. Build and deploy
cd backend
gcloud run deploy quiz-app-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SUPABASE_URL=your-url,SUPABASE_KEY=your-key
```

---

## 🎯 Recommended CLI Workflow

### For Quick Deployment (Render)
```bash
# 1. Install Render CLI
npm install -g @render/cli

# 2. Authenticate
render login

# 3. Deploy with our script
./deploy-render-cli.sh

# 4. Set environment variables in dashboard
# 5. Update frontend API URL
# 6. Test!
```

### For Full Control (DigitalOcean + Custom Script)
```bash
# 1. Create droplet
doctl compute droplet create quiz-app \
  --size s-1vcpu-1gb \
  --image ubuntu-22-04-x64 \
  --region nyc1 \
  --ssh-keys your-ssh-key-id

# 2. Deploy with our custom script
./deploy-vps.sh
```

### For Enterprise (AWS)
```bash
# 1. Setup infrastructure with Terraform
terraform init
terraform apply

# 2. Deploy with CodeDeploy
aws deploy create-deployment \
  --application-name quiz-app \
  --deployment-group-name production
```

---

## 📋 CLI Deployment Checklist

- [ ] CLI tool installed and authenticated
- [ ] Environment variables configured
- [ ] Database (Supabase) set up
- [ ] Frontend API URL updated
- [ ] CORS settings configured
- [ ] SSL/HTTPS enabled
- [ ] Domain configured (if custom)
- [ ] Monitoring set up
- [ ] Backup strategy in place

---

## 🚨 Troubleshooting

### Render CLI Issues
```bash
# Check authentication
render services --output text

# Re-authenticate
render login

# Check service status
render services
```

### Railway CLI Issues
```bash
# Check login status
railway whoami

# Re-login
railway login

# Check deployment logs
railway logs
```

### General Issues
```bash
# Check if service is running
curl -I https://your-app-url.com/api/me

# Check environment variables
# (In respective platform's dashboard)

# Check logs
# (Platform-specific log viewing commands)
```

---

## 🎉 Success!

Once deployed via CLI, your quiz app will be:
- ✅ Live on the internet
- ✅ Scalable to 700+ users
- ✅ Automatically deployed on git push
- ✅ Monitored and backed up

Choose the CLI that matches your preferred platform and deploy away! 🚀