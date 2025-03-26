# Ticket Booking Backend

A Django REST API for event ticket booking with user authentication and gender-based pricing.

## Built With
* Django
* Django Rest Framework

## Prerequisites
* Python 3.6 or higher
* Git

## Installation

### 1. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv env

# Activate on Windows
env\Scripts\activate

# Activate on Unix/MacOS
source env/bin/activate
```

### 2. Clone Repository
```bash
git clone https://github.com/maharshi-me/ticket-booking-backend.git
cd ticket-booking-backend
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Database
```bash
python manage.py migrate
```

### 5. Seed Database
```bash
python manage.py seed_data
```

### 6. Run Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register/` | Register new user |
| POST | `/api/users/login/` | User login |
| POST | `/api/users/logout/` | User logout |

### Events
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/events/` | List all events |
| GET | `/api/events/<id>/` | Get event details |
| POST | `/api/events/<id>/attend/` | Attend an event |
| POST | `/api/events/<id>/unattend/` | Unattend an event |

## Features
* User authentication
* Event listing and details
* Event attendance management
* Gender-based pricing (5% discount for female users)
* Timezone-aware event scheduling

### Note
- The API uses Django's session-based authentication
- CSRF token is required for POST requests
- Session cookie is required for authenticated requests

## Usage

### Django REST Framework Interface

The API provides a browsable interface for testing and development:

1. Start the development server:
```bash
python manage.py runserver
```

2. Open your browser and navigate to:
- Register: http://localhost:8000/api/users/register/
- Login: http://localhost:8000/api/users/login/
- Events List: http://localhost:8000/api/events/
- Event Details: http://localhost:8000/api/events/:id/


## Testing with Postman

### Import Collection
1. Open Postman
2. Click "Import" button
3. Select the `Tickets.postman_collection.json` file from project root
4. The collection will be imported with all API endpoints configured

### Available Requests
- Authentication
  - Register
  - Login
  - Logout
- Events
  - List Events
  - Get Event Details
  - Attend Event
  - Unattend Event

### Notes
- Collection variables handle CSRF tokens in POST requests
- Cookies are managed between requests automatically

