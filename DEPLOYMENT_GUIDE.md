# 🚀 Deployment Guide - Quiz App for 700+ Users

## Deployment Options Overview

| Platform | Backend | Frontend | Cost | Difficulty | Best For |
|----------|---------|----------|------|------------|----------|
| **Render** | ✅ | ✅ | Free/$7/mo | Easy | Quick deployment |
| **Railway** | ✅ | ✅ | $5/mo | Easy | Modern platform |
| **Vercel + Render** | Render | Vercel | Free | Easy | Best performance |
| **Netlify + Render** | Render | Netlify | Free | Easy | Great DX |
| **AWS (EC2)** | ✅ | ✅ | ~$10/mo | Medium | Full control |
| **DigitalOcean** | ✅ | ✅ | $6/mo | Medium | Simple VPS |
| **Heroku** | ✅ | ✅ | $7/mo | Easy | Classic choice |
| **Google Cloud Run** | ✅ | ✅ | Pay-as-go | Medium | Auto-scaling |

---

## 🌟 Recommended: Render (Easiest & Free)

### Why Render?
- ✅ Free tier available
- ✅ Auto-deploys from GitHub
- ✅ Built-in SSL certificates
- ✅ Easy environment variables
- ✅ Supports both backend and frontend

### Step-by-Step Deployment

#### 1. Deploy Backend on Render

1. **Go to [render.com](https://render.com)** and sign up
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**: `debugbyte007/quiz_app`
4. **Configure the service:**
   ```
   Name: quiz-app-backend
   Region: Choose closest to your users
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --config gunicorn.conf.py app:app
   ```

5. **Add Environment Variables:**
   ```
   SUPABASE_URL=https://prsncomvnxoxbcopqpmq.supabase.co
   SUPABASE_KEY=your-anon-key-here
   SECRET_KEY=generate-a-random-secret-key
   PORT=10000
   ```

6. **Choose Plan:**
   - Free: Good for testing
   - Starter ($7/mo): Recommended for 700 users

7. **Click "Create Web Service"**
8. **Wait 2-3 minutes** for deployment
9. **Copy your backend URL**: `https://quiz-app-backend.onrender.com`

#### 2. Deploy Frontend on Render

1. **Click "New +" → "Static Site"**
2. **Connect same repository**
3. **Configure:**
   ```
   Name: quiz-app-frontend
   Branch: main
   Root Directory: frontend
   Build Command: (leave empty)
   Publish Directory: .
   ```

4. **Click "Create Static Site"**
5. **Copy your frontend URL**: `https://quiz-app-frontend.onrender.com`

#### 3. Update Frontend API URL

Update `frontend/api.js`:
```javascript
const API_BASE = "https://quiz-app-backend.onrender.com/api";
```

Commit and push:
```bash
git add frontend/api.js
git commit -m "Update API URL for production"
git push origin main
```

Render will auto-deploy!

---

## 🚀 Option 2: Vercel (Frontend) + Render (Backend)

### Why This Combo?
- ✅ Vercel: Best frontend performance (CDN)
- ✅ Render: Reliable backend hosting
- ✅ Both have generous free tiers

### Deploy Backend on Render
Follow steps from Option 1 above.

### Deploy Frontend on Vercel

1. **Go to [vercel.com](https://vercel.com)** and sign up
2. **Click "Add New" → "Project"**
3. **Import your GitHub repository**
4. **Configure:**
   ```
   Framework Preset: Other
   Root Directory: frontend
   Build Command: (leave empty)
   Output Directory: .
   ```

5. **Add Environment Variable:**
   ```
   VITE_API_BASE=https://quiz-app-backend.onrender.com/api
   ```

6. **Click "Deploy"**
7. **Your app will be live at**: `https://quiz-app-xxx.vercel.app`

---

## 🐳 Option 3: Railway (All-in-One)

### Why Railway?
- ✅ Modern platform
- ✅ Simple deployment
- ✅ $5/month for everything
- ✅ Great for 700+ users

### Deployment Steps

1. **Go to [railway.app](https://railway.app)** and sign up
2. **Click "New Project" → "Deploy from GitHub repo"**
3. **Select your repository**
4. **Railway auto-detects Python**
5. **Add Environment Variables:**
   ```
   SUPABASE_URL=your-url
   SUPABASE_KEY=your-key
   SECRET_KEY=your-secret
   ```

6. **Configure Start Command:**
   ```
   cd backend && gunicorn --config gunicorn.conf.py app:app
   ```

7. **Deploy!** Railway handles everything

---

## 💻 Option 4: DigitalOcean Droplet (VPS)

### Why DigitalOcean?
- ✅ Full control
- ✅ $6/month for 1GB RAM
- ✅ Can handle 700+ users easily
- ✅ SSH access

### Deployment Steps

1. **Create Droplet**
   - OS: Ubuntu 22.04
   - Plan: Basic $6/mo (1GB RAM)
   - Region: Closest to users

2. **SSH into server:**
   ```bash
   ssh root@your-droplet-ip
   ```

3. **Install dependencies:**
   ```bash
   apt update
   apt install python3-pip python3-venv nginx -y
   ```

4. **Clone repository:**
   ```bash
   cd /var/www
   git clone https://github.com/debugbyte007/quiz_app.git
   cd quiz_app
   ```

5. **Setup backend:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Create .env file:**
   ```bash
   nano .env
   # Add your Supabase credentials
   ```

7. **Setup systemd service:**
   ```bash
   nano /etc/systemd/system/quiz-app.service
   ```

   ```ini
   [Unit]
   Description=Quiz App Backend
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/var/www/quiz_app/backend
   Environment="PATH=/var/www/quiz_app/backend/venv/bin"
   ExecStart=/var/www/quiz_app/backend/venv/bin/gunicorn --config gunicorn.conf.py app:app

   [Install]
   WantedBy=multi-user.target
   ```

8. **Start service:**
   ```bash
   systemctl enable quiz-app
   systemctl start quiz-app
   ```

9. **Configure Nginx:**
   ```bash
   nano /etc/nginx/sites-available/quiz-app
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       # Frontend
       location / {
           root /var/www/quiz_app/frontend;
           try_files $uri $uri/ /index.html;
       }

       # Backend API
       location /api {
           proxy_pass http://localhost:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

10. **Enable site:**
    ```bash
    ln -s /etc/nginx/sites-available/quiz-app /etc/nginx/sites-enabled/
    nginx -t
    systemctl restart nginx
    ```

11. **Setup SSL (Optional but recommended):**
    ```bash
    apt install certbot python3-certbot-nginx -y
    certbot --nginx -d your-domain.com
    ```

---

## ☁️ Option 5: AWS EC2 (Enterprise)

### Why AWS?
- ✅ Enterprise-grade
- ✅ Highly scalable
- ✅ Many regions worldwide
- ✅ ~$10/month (t3.small)

### Quick Setup

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04
   - Instance Type: t3.small (2GB RAM)
   - Security Group: Allow ports 22, 80, 443

2. **Follow DigitalOcean steps above** (same process)

3. **Use Elastic IP** for static IP address

4. **Optional: Use RDS** for database instead of Supabase

---

## 🎯 Recommended Setup for 700 Users

### Budget Option (Free - $7/mo)
```
Frontend: Vercel (Free)
Backend: Render Starter ($7/mo)
Database: Supabase Free Tier
Total: $7/month
```

### Performance Option ($12/mo)
```
Frontend: Vercel Pro ($20/mo) or Netlify (Free)
Backend: Render Standard ($25/mo) or DigitalOcean ($6/mo)
Database: Supabase Pro ($25/mo)
Total: $12-50/month
```

### Enterprise Option ($50+/mo)
```
Frontend: AWS CloudFront + S3
Backend: AWS EC2 (t3.medium)
Database: Supabase Pro or AWS RDS
Load Balancer: AWS ALB
Total: $50-100/month
```

---

## 📋 Pre-Deployment Checklist

- [ ] Supabase database tables created
- [ ] Environment variables configured
- [ ] Frontend API URL updated
- [ ] CORS settings configured for production domain
- [ ] SSL certificate enabled (HTTPS)
- [ ] Session cookies configured for production
- [ ] Test with multiple users
- [ ] Monitor performance

---

## 🔧 Post-Deployment

### Update CORS in backend/app.py

```python
CORS(
    app,
    supports_credentials=True,
    resources={
        r"/api/*": {
            "origins": [
                "https://your-frontend-domain.com",
                "http://localhost:5500",  # for local testing
            ]
        }
    },
)
```

### Update Session Cookies for Production

```python
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,  # Required for HTTPS
)
```

---

## 🎉 You're Ready!

Choose the option that fits your needs and budget. For 700 users, I recommend:

**Best Value**: Render ($7/mo) - Easy and reliable
**Best Performance**: Vercel + Render ($7/mo) - Fast CDN
**Full Control**: DigitalOcean ($6/mo) - VPS with SSH access

Need help with deployment? Check the platform-specific guides above!
