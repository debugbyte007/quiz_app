from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os
import random
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

CORS(
    app,
    supports_credentials=True,
    resources={
        r"/api/*": {
            "origins": [
                "https://quiz-app-sdc.netlify.app",
                "http://localhost:5500",
            ]
        }
    },
)

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
)

# -----------------------
# In-memory storage
# -----------------------

users_collection = []
quizzes_collection = []
results_collection = []

# -----------------------
# Frontend Routes
# -----------------------

@app.route("/")
def root():
    return send_from_directory(FRONTEND_DIR, "login.html")


@app.route("/home")
def home_page():
    return send_from_directory(FRONTEND_DIR, "index.html")


# -----------------------
# Utility
# -----------------------

def _generate_code(length=5):
    chars = string.digits
    while True:
        code = "".join(random.choice(chars) for _ in range(length))
        if not any(q["code"] == code for q in quizzes_collection):
            return code


# -----------------------
# AUTH
# -----------------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    existing = next((u for u in users_collection if u["username"].lower() == username.lower()), None)

    if existing:
        return jsonify({"error": "Username already exists"}), 400

    user = {
        "username": username,
        "password_hash": generate_password_hash(password),
        "created_at": datetime.utcnow().isoformat() + "Z",
    }

    users_collection.append(user)
    session["username"] = username

    return jsonify({"message": "Registered successfully", "username": username})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = next((u for u in users_collection if u["username"].lower() == username.lower()), None)

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    session["username"] = user["username"]

    return jsonify({"message": "Logged in", "username": user["username"]})


@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    return jsonify({"message": "Logged out"})


@app.route("/api/me", methods=["GET"])
def me():
    username = session.get("username")

    if not username:
        return jsonify({"authenticated": False}), 200

    return jsonify({"authenticated": True, "username": username})


# -----------------------
# QUIZ CREATION
# -----------------------

@app.route("/api/quizzes", methods=["POST"])
def create_quiz():

    username = session.get("username")

    if not username:
        return jsonify({"error": "Authentication required"}), 401

    payload = request.json or {}

    title = payload.get("title", "Untitled Quiz").strip()
    time_mode = payload.get("time_mode", "per_quiz")
    time_limit = int(payload.get("time_limit", 60))
    questions = payload.get("questions", [])

    if not questions:
        return jsonify({"error": "At least one question required"}), 400

    code = _generate_code()

    quiz = {
        "code": code,
        "title": title,
        "host": username,
        "time_mode": time_mode,
        "time_limit": time_limit,
        "questions": questions,
        "status": "lobby",
        "players": [],
        "created_at": datetime.utcnow().isoformat() + "Z",
        "started_at": None,
    }

    quizzes_collection.append(quiz)

    return jsonify({"code": code, "quiz": quiz})


@app.route("/api/quizzes/<code>", methods=["GET"])
def get_quiz(code):

    quiz = next((q for q in quizzes_collection if q["code"] == code), None)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    sanitized_questions = []

    for idx, q in enumerate(quiz["questions"]):
        sanitized_questions.append({
            "index": idx,
            "text": q.get("text"),
            "options": q.get("options", []),
            "points": q.get("points", 1),
        })

    return jsonify({
        "code": quiz["code"],
        "title": quiz["title"],
        "host": quiz["host"],
        "time_mode": quiz["time_mode"],
        "time_limit": quiz["time_limit"],
        "status": quiz["status"],
        "questions": sanitized_questions,
    })


@app.route("/api/quizzes/<code>/players", methods=["GET"])
def get_players(code):

    quiz = next((q for q in quizzes_collection if q["code"] == code), None)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    return jsonify({"players": quiz["players"]})


@app.route("/api/quizzes/<code>/join", methods=["POST"])
def join_quiz(code):

    username = session.get("username")

    if not username:
        return jsonify({"error": "Authentication required"}), 401

    quiz = next((q for q in quizzes_collection if q["code"] == code), None)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    if username not in quiz["players"]:
        quiz["players"].append(username)

    return jsonify({"message": "Joined quiz", "players": quiz["players"]})


@app.route("/api/quizzes/<code>/start", methods=["POST"])
def start_quiz(code):

    username = session.get("username")

    quiz = next((q for q in quizzes_collection if q["code"] == code), None)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    if quiz["host"] != username:
        return jsonify({"error": "Only host can start quiz"}), 403

    quiz["status"] = "started"
    quiz["started_at"] = datetime.utcnow().isoformat() + "Z"

    return jsonify({"message": "Quiz started"})


# -----------------------
# SUBMIT QUIZ
# -----------------------

@app.route("/api/quizzes/<code>/submit", methods=["POST"])
def submit_quiz(code):

    username = session.get("username")

    quiz = next((q for q in quizzes_collection if q["code"] == code), None)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    payload = request.json or {}

    answers = payload.get("answers", [])
    total_time = float(payload.get("total_time", 0))

    questions = quiz["questions"]

    total_points = 0
    correct_count = 0
    detailed = []

    for item in answers:

        idx = item.get("index")
        selected = item.get("selected", [])

        q = questions[idx]

        correct = sorted(q.get("correct_indices", []))

        is_correct = sorted(selected) == correct

        points = q.get("points", 1) if is_correct else 0

        if is_correct:
            correct_count += 1
            total_points += points

        detailed.append({
            "question": q.get("text"),
            "selected": selected,
            "correct": correct,
            "is_correct": is_correct
        })

    result = {
        "code": code,
        "username": username,
        "total_points": total_points,
        "correct_count": correct_count,
        "total_questions": len(questions),
        "total_time": total_time,
        "details": detailed
    }

    results_collection.append(result)

    return jsonify({"result": result})


@app.route("/api/quizzes/<code>/leaderboard", methods=["GET"])
def leaderboard(code):

    filtered = [r for r in results_collection if r["code"] == code]

    filtered = sorted(filtered, key=lambda x: (-x["correct_count"], x["total_time"]))

    for i, r in enumerate(filtered, start=1):
        r["rank"] = i

    return jsonify({"leaderboard": filtered})


@app.route("/api/history", methods=["GET"])
def history():

    username = session.get("username")

    user_results = [r for r in results_collection if r["username"] == username]

    return jsonify({"results": user_results})


# -----------------------
# Run Server
# -----------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)