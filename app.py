import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'festful_secret_key'  # Change this in production
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'festful.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- ROUTES ---
@app.route('/')
def home():
    conn = get_db()
    events = conn.execute('SELECT * FROM Events WHERE status = "upcoming" ORDER BY event_start').fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/events')
def show_events():
    conn = get_db()
    events = conn.execute('SELECT * FROM Events ORDER BY event_start').fetchall()
    conn.close()
    return render_template('events.html', events=events)

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if 'role' not in session or session['role'] not in ['admin', 'organizer']:
        flash('Only organizers/admins can add events.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        event_start = request.form['event_start']
        venue = request.form['venue']
        college = request.form['college']
        club_name = request.form['club_name']
        conn = get_db()
        conn.execute('''INSERT INTO Events (title, description, event_start, venue, category, status, club_id)
                        VALUES (?, ?, ?, ?, ?, 'upcoming', (SELECT club_id FROM Clubs WHERE club_name=? LIMIT 1))''',
                     (title, description, event_start, venue, college, club_name, club_name))
        conn.commit()
        conn.close()
        flash('Event added successfully!')
        return redirect(url_for('home'))
    return render_template('add_event.html')

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    if 'role' not in session or session['role'] not in ['admin', 'organizer']:
        flash('Only organizers/admins can delete events.')
        return redirect(url_for('login'))
    conn = get_db()
    conn.execute('DELETE FROM Events WHERE event_id=?', (event_id,))
    conn.commit()
    conn.close()
    flash('Event deleted!')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        hashed_pw = generate_password_hash(password)
        conn = get_db()
        try:
            conn.execute('INSERT INTO Users (name, email, password, role) VALUES (?, ?, ?, ?)',
                         (name, email, hashed_pw, role))
            conn.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered.')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        user = conn.execute('SELECT * FROM Users WHERE email=?', (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.')
    return redirect(url_for('home'))

@app.route('/register_event/<int:event_id>', methods=['POST'])
def register_event(event_id):
    if 'user_id' not in session:
        flash('Please login to register for events.')
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = get_db()
    try:
        conn.execute('INSERT INTO Registrations (user_id, event_id) VALUES (?, ?)', (user_id, event_id))
        conn.commit()
        flash('Registered for event!')
    except sqlite3.IntegrityError:
        flash('Already registered for this event.')
    finally:
        conn.close()
    return redirect(url_for('home'))

@app.route('/add_winners/<int:event_id>', methods=['GET', 'POST'])
def add_winners(event_id):
    if 'role' not in session or session['role'] not in ['admin', 'organizer']:
        flash('Only organizers/admins can add winners.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        winner_name = request.form['winner_name']
        position = request.form['position']
        conn = get_db()
        user = conn.execute('SELECT user_id FROM Users WHERE name=?', (winner_name,)).fetchone()
        if user:
            conn.execute('INSERT INTO Winners (event_id, user_id, position) VALUES (?, ?, ?)',
                         (event_id, user['user_id'], position))
            conn.commit()
            flash('Winner added!')
        else:
            flash('User not found.')
        conn.close()
        return redirect(url_for('home'))
    return '''<form method="post">
                Winner Name: <input name="winner_name" required><br>
                Position: <input name="position" required><br>
                <button type="submit">Add Winner</button>
              </form>'''

# --- DB INIT (for first run) ---
def init_db():
    conn = get_db()
    with open('festful_schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)