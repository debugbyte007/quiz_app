from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os
import random
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from db import users_collection, quizzes_collection, results_collection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

app = Flask(__name__)
# For production, set this via environment variable on Render
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

# ✅ CORS: allow your Netlify frontend + local dev, with credentials
CORS(
    app,
    supports_credentials=True,
    resources={
        r"/api/*": {
            "origins": [
                "https://quiz-app-sdc.netlify.app",  # your Netlify URL
                "http://localhost:5500",             # optional: local testing (Live Server)
            ]
        }
    },
)

# ✅ Cookies: allow cross-site cookies over HTTPS
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
)


@app.route("/")
def root():
    # default to login page
    return send_from_directory(FRONTEND_DIR, "login.html")


@app.route("/home")
def home_page():
    return send_from_directory(FRONTEND_DIR, "index.html")


def _generate_code(length=5):
    chars = string.digits
    while True:
        code = "".join(random.choice(chars) for _ in range(length))
        if not quizzes_collection.find_one({"code": code}):
            return code


# ---------- AUTH ----------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if users_collection.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}}):
        return jsonify({"error": "Username already exists"}), 400

    user = {
        "username": username,
        "password_hash": generate_password_hash(password),
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    users_collection.insert_one(user)
    session["username"] = username

    return jsonify({"message": "Registered successfully", "username": username})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = users_collection.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})

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
    return jsonify({"authenticated": True, "username": username}), 200


# ---------- QUIZ CREATION & MANAGEMENT ----------

@app.route("/api/quizzes", methods=["POST"])
def create_quiz():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Authentication required"}), 401

    payload = request.json or {}
    title = payload.get("title", "Untitled Quiz").strip() or "Untitled Quiz"
    time_mode = payload.get("time_mode", "per_quiz")
    time_limit = int(payload.get("time_limit", 60))
    questions = payload.get("questions", [])

    if not questions:
        return jsonify({"error": "At least one question is required"}), 400

    for q in questions:
        if not q.get("text") or not q.get("options"):
            return jsonify({"error": "Each question needs text and options"}), 400

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
    quizzes_collection.insert_one(quiz)

    return jsonify({"code": code, "quiz": quiz})


@app.route("/api/quizzes/<code>", methods=["GET"])
def get_quiz(code):
    quiz = quizzes_collection.find_one({"code": code})
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
    quiz = quizzes_collection.find_one({"code": code})
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404
    return jsonify({"players": quiz.get("players", [])})


@app.route("/api/quizzes/<code>/join", methods=["POST"])
def join_quiz(code):
    username = session.get("username")
    if not username:
        return jsonify({"error": "Authentication required"}), 401

    quiz = quizzes_collection.find_one({"code": code})
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    if quiz["status"] == "ended":
        return jsonify({"error": "Quiz has already ended"}), 400

    if username not in quiz["players"]:
        quizzes_collection.update_one({"code": code}, {"$push": {"players": username}})
        quiz["players"].append(username)

    return jsonify({"message": "Joined quiz", "code": code, "players": quiz["players"]})


@app.route("/api/quizzes/<code>/start", methods=["POST"])
def start_quiz(code):
    username = session.get("username")
    if not username:
        return jsonify({"error": "Authentication required"}), 401

    quiz = quizzes_collection.find_one({"code": code})
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404
    if quiz["host"] != username:
        return jsonify({"error": "Only the host can start the quiz"}), 403
    if quiz["status"] != "lobby":
        return jsonify({"error": "Quiz already started or ended"}), 400

    quizzes_collection.update_one(
        {"code": code},
        {"$set": {"status": "started", "started_at": datetime.utcnow().isoformat() + "Z"}}
    )

    return jsonify({"message": "Quiz started"})


@app.route("/api/quizzes/<code>/submit", methods=["POST"])
def submit_quiz(code):
    username = session.get("username")
    if not username:
        return jsonify({"error": "Authentication required"}), 401

    quiz = quizzes_collection.find_one({"code": code})
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    payload = request.json or {}
    answers = payload.get("answers", [])
    total_time = float(payload.get("total_time", 0.0))

    questions = quiz["questions"]
    total_points = 0
    correct_count = 0
    detailed = []

    for item in answers:
        idx = int(item.get("index", -1))
        selected = item.get("selected", [])
        if idx < 0 or idx >= len(questions):
            continue
        q = questions[idx]
        correct_indices = sorted(q.get("correct_indices", []))
        selected_sorted = sorted(selected)
        is_correct = correct_indices == selected_sorted
        points = int(q.get("points", 1)) if is_correct else 0
        if is_correct:
            correct_count += 1
            total_points += points
        detailed.append({
            "index": idx,
            "question": q.get("text"),
            "options": q.get("options", []),
            "selected": selected,
            "correct_indices": correct_indices,
            "is_correct": is_correct,
            "points": points,
        })

    entry = {
        "code": code,
        "username": username,
        "total_points": total_points,
        "correct_count": correct_count,
        "total_questions": len(questions),
        "total_time": total_time,
        "submitted_at": datetime.utcnow().isoformat() + "Z",
        "details": detailed,
    }
    results_collection.insert_one(entry)

    return jsonify({"result": entry})


@app.route("/api/quizzes/<code>/leaderboard", methods=["GET"])
def leaderboard(code):
    filtered = list(results_collection.find({"code": code}, {"_id": 0}).sort([("correct_count", -1), ("total_time", 1)]))
    for i, r in enumerate(filtered, start=1):
        r["rank"] = i
    return jsonify({"leaderboard": filtered})


@app.route("/api/history", methods=["GET"])
def history():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Authentication required"}), 401
    user_results = list(results_collection.find({"username": username}, {"_id": 0}))
    return jsonify({"results": user_results})


if __name__ == "__main__":
    # Local dev: you can still run this directly
    app.run(host="0.0.0.0", port=5001, debug=True)
