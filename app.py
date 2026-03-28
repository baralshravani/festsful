import os
from datetime import datetime # 1. CRITICAL: Don't forget this import!
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- DATABASE CONFIG ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'festful.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELS ---
class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String)

class Event(db.Model):
    __tablename__ = 'Events'
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    venue = db.Column(db.String)
    category = db.Column(db.String)
    event_start = db.Column(db.DateTime)
    status = db.Column(db.String, default='upcoming')

# --- ROUTES ---

@app.route('/')
def home():
    # Fetch events to display on your black/yellow landing page
    events = Event.query.filter_by(status='upcoming').all()
    return render_template('index.html', events=events)

@app.route('/seed')
def seed_data():
    try:
        # 1. Add a sample User
        new_user = User(name="Shravani", role="admin", email="test@festful.com")
        db.session.add(new_user)
        
        # 2. Add Pune Events
        e1 = Event(title="Hinjewadi Tech Hack", venue="Pimpri, Pune", category="Tech", 
                   event_start=datetime(2026, 4, 15, 10, 0))
        e2 = Event(title="Kothrud Dance Night", venue="Kothrud, Pune", category="Cultural", 
                   event_start=datetime(2026, 4, 20, 18, 0))
        
        db.session.add_all([e1, e2])
        db.session.commit()
        return "<h1>Success!</h1><p>Pune events added. <a href='/'>Go to Home</a></p>"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)