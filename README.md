# FestFul Event Management System

A complete Flask-based web application for managing college events with user authentication and role-based access control.

## Features

### For Students
- View upcoming events
- Register for events
- User registration and login

### For Organizers/Admins
- All student features plus:
- Add new events
- Delete events
- Add event winners

## Project Structure

```
festful/
├── app.py                    # Main Flask application
├── festful.db               # SQLite database
├── festful_schema.sql       # Database schema
├── requirements.txt         # Python dependencies
├── templates/               # HTML templates
│   ├── index.html          # Home page
│   ├── events.html         # All events page
│   ├── add_event.html      # Add event form
│   ├── register.html       # User registration
│   └── login.html          # User login
└── static/                  # Static files
    └── style.css           # CSS styles
```

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   python app.py
   ```

3. **Access the Application:**
   Open your browser and go to `http://127.0.0.1:5000`

## Database Schema

The application uses SQLite with the following tables:
- **Users**: User accounts with roles (student, organizer, admin)
- **Clubs**: College clubs
- **Events**: Event information
- **Registrations**: User event registrations
- **Winners**: Event winners

## API Routes

### Public Routes
- `GET /` - Home page with upcoming events
- `GET /events` - All events
- `GET /register` - User registration form
- `POST /register` - Register new user
- `GET /login` - Login form
- `POST /login` - User login
- `GET /logout` - Logout

### Protected Routes (Login Required)
- `POST /register_event/<event_id>` - Register for event

### Organizer/Admin Routes
- `GET /add_event` - Add event form
- `POST /add_event` - Create new event
- `POST /delete_event/<event_id>` - Delete event
- `GET /add_winners/<event_id>` - Add winners form
- `POST /add_winners/<event_id>` - Add event winners

## User Roles

1. **Student**: Can view events and register for them
2. **Organizer**: Can create and manage events, add winners
3. **Admin**: Full access to all features

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- Input validation
- SQL injection protection via parameterized queries

## Development

The application runs in debug mode by default. For production deployment:

1. Change the secret key in `app.py`
2. Set `app.debug = False`
3. Use a production WSGI server like Gunicorn
4. Configure proper session storage

## Sample Data

To add sample data, you can register users and add events through the web interface, or modify the database directly using SQLite browser.

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, Jinja2 templates
- **Security**: Werkzeug (password hashing), Flask sessions