-- Supabase SQL Schema for Quiz App
-- Run these commands in your Supabase SQL Editor

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Quizzes table
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    host VARCHAR(255) NOT NULL,
    time_mode VARCHAR(50) DEFAULT 'per_quiz',
    time_limit INTEGER DEFAULT 60,
    questions JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'lobby',
    players TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE
);

-- Results table
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) NOT NULL,
    username VARCHAR(255) NOT NULL,
    total_points INTEGER DEFAULT 0,
    correct_count INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 0,
    total_time DECIMAL(10,2) DEFAULT 0.0,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    details JSONB
);

-- Indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_quizzes_code ON quizzes(code);
CREATE INDEX idx_quizzes_host ON quizzes(host);
CREATE INDEX idx_results_code ON results(code);
CREATE INDEX idx_results_username ON results(username);
CREATE INDEX idx_results_correct_count ON results(correct_count);

-- Row Level Security (RLS) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE quizzes ENABLE ROW LEVEL SECURITY;
ALTER TABLE results ENABLE ROW LEVEL SECURITY;

-- Allow all operations for now (you can make this more restrictive later)
CREATE POLICY "Allow all operations on users" ON users FOR ALL USING (true);
CREATE POLICY "Allow all operations on quizzes" ON quizzes FOR ALL USING (true);
CREATE POLICY "Allow all operations on results" ON results FOR ALL USING (true);