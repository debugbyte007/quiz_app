#!/bin/bash
# Production deployment script for Quiz App

echo "🚀 Deploying Quiz App for 700+ users..."

# Install dependencies
echo "📦 Installing dependencies..."
cd backend
pip install -r requirements.txt
pip install gunicorn

# Check environment variables
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
    echo "⚠️  Warning: Supabase credentials not found!"
    echo "   Using JSON files for local development"
    echo "   For 700+ users, please set up Supabase:"
    echo "   export SUPABASE_URL=your_project_url"
    echo "   export SUPABASE_KEY=your_anon_key"
fi

# Start production server
echo "🔥 Starting production server with Gunicorn..."
gunicorn --config gunicorn.conf.py app:app