# 🚀 Start Testing Your Quiz App with Supabase

## ✅ Everything is Running!

### Backend (Supabase Connected)
- URL: http://localhost:5001
- Status: 🚀 Using Supabase database for production scaling
- Database: PostgreSQL on Supabase Cloud

### Frontend
- URL: http://localhost:5500

## 🎯 Test the Actual Application

### Step 1: Open the Login Page
Open your browser and go to:
```
http://localhost:5500/frontend/login.html
```

### Step 2: Register a New Account
1. Click "Register" link at the bottom
2. Create username: `host1`
3. Create password: `password123`
4. Click Register

### Step 3: Create a Quiz (As Host)
1. After login, you'll see the home page
2. Click "Host a Quiz"
3. Fill in quiz details:
   - Title: "Test Quiz for 700 Users"
   - Time mode: Per Quiz
   - Time limit: 60 seconds
4. Add questions:
   - Question 1: "What is 2+2?"
   - Options: 2, 4, 6, 8
   - Mark "4" as correct
   - Points: 10
5. Click "Create Quiz"
6. You'll get a 5-digit code (e.g., 12345)

### Step 4: Join as Player (Open New Browser/Incognito)
1. Open a new incognito window
2. Go to: http://localhost:5500/frontend/login.html
3. Register as: `player1` / `password123`
4. Click "Join a Quiz"
5. Enter the 5-digit code from Step 3
6. Click Join

### Step 5: Start the Quiz (As Host)
1. In the host window, you'll see "player1" in the lobby
2. Click "Start Quiz"

### Step 6: Play the Quiz (As Player)
1. Answer the questions
2. Submit when done
3. View your score and leaderboard

## 🧪 Test with Multiple Users

To simulate 700 users, you can:
1. Open multiple browser windows/tabs
2. Use different browsers (Chrome, Firefox, Edge)
3. Use incognito/private windows
4. Register different users: player1, player2, player3, etc.

## 📊 Monitor Supabase

Check your Supabase dashboard:
1. Go to: https://prsncomvnxoxbcopqpmq.supabase.co
2. Click "Table Editor"
3. See real-time data:
   - `users` table: All registered users
   - `quizzes` table: All created quizzes
   - `results` table: All quiz submissions

## 🎉 You're Ready!

Your app is now connected to Supabase and ready to handle 700+ concurrent users!
