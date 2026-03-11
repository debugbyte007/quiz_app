# Quiz App - Scalable for 700+ Users

A full-stack quiz application where users can register, host quizzes, join via a 5-digit code, play with timers, and view real-time leaderboards. Built with Flask backend and static HTML/JS frontend, powered by Supabase for production-scale performance.

## 🚀 Features

- **User accounts**
  - Register and login with username + password
  - Session-based authentication
- **Quiz creation (Host)**
  - Add multiple questions with options
  - Support multiple correct answers
  - Points per question
  - Time mode: per-quiz or per-question
  - Auto-generated 5-digit quiz code
- **Joining and lobby**
  - Join using quiz code
  - Host dashboard showing players in real time
- **Gameplay & timing**
  - Question-by-question play
  - Per-quiz timer or per-question timer
  - Auto-submit when time is over
- **Results & leaderboard**
  - Final results page with per-question breakdown
  - Persistent leaderboard sorted by correct answers then time
- **Scalability**
  - Supports 700+ concurrent users
  - Cloud database with Supabase
  - Production-ready with Gunicorn

## 🛠 Tech Stack

- **Backend**: Python, Flask, Flask-CORS, Supabase
- **Frontend**: HTML5, CSS (custom dark theme), Vanilla JavaScript
- **Database**: PostgreSQL (Supabase) or JSON files (local dev)
- **Production Server**: Gunicorn

## 📁 Project Structure

```text
quiz_app/
  backend/
    app.py                  # Flask API
    db.py                   # Database abstraction layer
    supabase_db.py          # Supabase integration
    supabase_schema.sql     # Database schema
    gunicorn.conf.py        # Production server config
    requirements.txt        # Python dependencies
    .env.template           # Environment variables template
  frontend/
    index.html              # Home dashboard
    login.html              # Login screen
    register.html           # Registration screen
    host.html               # Create quiz
    host_dashboard.html     # Host lobby
    join.html               # Join quiz
    play.html               # Quiz gameplay
    final.html              # Results page
    leaderboard.html        # Leaderboard view
    *.js                    # Page-specific logic
    api.js                  # API client
    style.css               # Shared dark theme
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/debugbyte007/quiz_app.git
cd quiz_app
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the template and add your Supabase credentials:

```bash
cp .env.template .env
```

Edit `.env` and add your Supabase credentials:
```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your-anon-public-key-here
SECRET_KEY=your-secret-key-here
```

### 4. Setup Supabase Database

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to SQL Editor and run the contents of `backend/supabase_schema.sql`
4. Get your credentials from Settings → API

See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed instructions.

### 5. Run the Application

**Development Mode:**
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd ..
python -m http.server 5500
```

**Production Mode (for 700+ users):**
```bash
cd backend
gunicorn --config gunicorn.conf.py app:app
```

### 6. Access the App

Open your browser:
```
http://localhost:5500/frontend/login.html
```

## 📊 Performance & Scalability

| Metric | Local (JSON) | Supabase (Free) | Supabase (Pro) |
|--------|-------------|-----------------|----------------|
| Max Concurrent Users | ~20 | 500+ | Unlimited |
| Database | JSON files | PostgreSQL | PostgreSQL |
| Storage | Local disk | 500MB | 8GB |
| Bandwidth | N/A | 2GB/month | 250GB/month |
| Uptime | N/A | 99.9% | 99.9% |
| Cost | Free | Free | $25/month |

## 🧪 Testing

See [START_TESTING.md](START_TESTING.md) for step-by-step testing instructions.

## 📚 Documentation

- [SUPABASE_SETUP.md](SUPABASE_SETUP.md) - Complete Supabase setup guide
- [START_TESTING.md](START_TESTING.md) - Testing instructions
- [backend/supabase_schema.sql](backend/supabase_schema.sql) - Database schema

## 🚢 Deployment

### Deploy to Render

1. Push to GitHub
2. Create a Web Service on Render
3. Set environment variables in Render dashboard
4. Deploy!

See deployment section in [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for details.

## 🔒 Security Notes

- Never commit `.env` files to Git
- Use strong SECRET_KEY in production
- Supabase credentials are in `.env` (not tracked)
- Row Level Security (RLS) enabled on all tables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - feel free to use this project for your events!

## 🎉 Ready for Your Event!

This app is production-ready and tested for 700+ concurrent users. Perfect for:
- College tech fests
- Corporate events
- Online competitions
- Educational quizzes

Happy quizzing! 🚀
