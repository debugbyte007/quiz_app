# Quiz App

A full-stack quiz application where users can register, host quizzes, join via a 5-digit code, play with timers, and view real-time leaderboards. Built with a Flask backend and a static HTML/JS frontend.

## Features

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
  - Per-quiz timer **or** per-question timer
  - Auto-submit when time is over for the quiz or a question
- **Results & leaderboard**
  - Final results page with per-question breakdown
  - Persistent leaderboard sorted by correct answers then time
- **Persistence**
  - All data stored in JSON files on the server

## Tech Stack

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: HTML5, CSS (custom dark theme), Vanilla JavaScript
- **Storage**: JSON files under `backend/data`

---

## Project Structure

```text
quiz_app/
  backend/
    app.py              # Flask API
    requirements.txt    # Python dependencies
    data/
      users.json        # user accounts
      quizzes.json      # quizzes and lobby state
      results.json      # quiz attempts & scores
  frontend/
    index.html          # authenticated home (host/join)
    login.html          # login screen
    register.html       # registration screen
    host.html           # create/manage quiz
    host_dashboard.html # host lobby dashboard
    join.html           # join quiz
    play.html           # quiz gameplay
    final.html          # results page
    leaderboard.html    # leaderboard view
    *.js                # page-specific logic
    style.css           # shared dark theme
```

---

## Running Locally

### 1. Backend (Flask)

From `quiz_app/backend`:

```bash
python -m venv venv
venv/Scripts/activate  # Windows PowerShell: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The API will run at `http://localhost:5001`.

### 2. Frontend (static server)

From `quiz_app/frontend`:

```bash
python -m http.server 5500
```

Open the app in your browser:

```text
http://localhost:5500/login.html
```

Flow:

1. Register on `register.html` (link from login page).
2. Login on `login.html`.
3. After login you land on `index.html` (home dashboard) where you can host or join quizzes.

---

## Deployment Notes (Render Example)

1. Add a `Procfile` in `backend/`:

   ```text
   web: gunicorn app:app
   ```

2. Ensure `gunicorn` is in `backend/requirements.txt`.
3. Push the project to GitHub.
4. Create a **Web Service** on Render pointing to `backend/`.
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Create a **Static Site** on Render pointing to `frontend/`.
6. Update all `API_BASE` constants in frontend JS files to your Render backend URL, e.g.:

   ```js
   const API_BASE = "https://your-backend.onrender.com/api";
   ```

---

## Customization Ideas

- Swap JSON storage for a real database (SQLite/PostgreSQL).
- Add more question types (text, numeric, etc.).
- Enhance results page with charts or badges.
- Add admin view for managing past quizzes and users.
