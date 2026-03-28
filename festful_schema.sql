-- Enable foreign key support (Crucial for SQLite)
PRAGMA foreign_keys = ON;

-- =========================
-- 1. USERS TABLE
-- =========================
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, -- Ensure your backend hashes this!
    role TEXT CHECK(role IN ('student','organizer','admin')) NOT NULL DEFAULT 'student',
    college TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- 2. CLUBS TABLE
-- =========================
CREATE TABLE Clubs (
    club_id INTEGER PRIMARY KEY AUTOINCREMENT,
    club_name TEXT NOT NULL,
    college TEXT NOT NULL,
    description TEXT,
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    -- If a user is deleted, we set created_by to NULL but keep the club
    FOREIGN KEY (created_by) REFERENCES Users(user_id) ON DELETE SET NULL
);

-- =========================
-- 3. EVENTS TABLE
-- =========================
CREATE TABLE Events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    -- Combined into one DATETIME for easy sorting: 'YYYY-MM-DD HH:MM:SS'
    event_start DATETIME NOT NULL,
    venue TEXT,
    organizer_id INTEGER NOT NULL,
    club_id INTEGER,
    poster_url TEXT,
    -- Status allows you to hide events without deleting them
    status TEXT CHECK(status IN ('upcoming', 'ongoing', 'completed', 'cancelled')) DEFAULT 'upcoming',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (organizer_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES Clubs(club_id) ON DELETE CASCADE
);

-- =========================
-- 4. REGISTRATIONS TABLE
-- =========================
CREATE TABLE Registrations (
    registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_status TEXT CHECK(payment_status IN ('pending', 'paid', 'refunded')) DEFAULT 'pending',
    attendance TEXT CHECK(attendance IN ('marked', 'not_marked')) DEFAULT 'not_marked',

    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE,

    -- Prevents a user from signing up for the same event twice
    UNIQUE(user_id, event_id)
);

-- =========================
-- 5. WINNERS TABLE
-- =========================
CREATE TABLE Winners (
    winner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL, -- Now links to the actual user profile
    position INTEGER NOT NULL, -- Use numbers (1, 2, 3) for easier logic
    prize_description TEXT,

    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- =========================
-- 6. INDEXES (For Performance)
-- =========================
-- These make searching for events by date or users by email much faster
CREATE INDEX idx_event_date ON Events(event_start);
CREATE INDEX idx_user_email ON Users(email);