# Loan Manager

Loan Manager is a Django REST Framework-based API for managing loans, user authentication, and administrative tasks. It allows users to register, verify their email with OTP, obtain JWT tokens, create and manage loans, foreclose loans, and provides admin-only views to oversee all loans and users.

## Features

- **User Management**: Register users with email OTP verification, login/logout with JWT cookies.
- **Loan Management**: Create loans, retrieve user-specific loans, foreclose loans, delete loans.
- **Admin Features**: View all loans, view all users with their loans, restricted to admin role.
- **Security**: JWT-based authentication with cookies, role-based access control (admin vs. user).

## Live Deployment

The backend is deployed on Render and accessible at:  
**https://loan-manager-qiu6.onrender.com/**

## Prerequisites

- **Python**: 3.8 or higher
- **Django**: 4.x
- **Django REST Framework**: Latest version
- **Simple JWT**: For token-based authentication
- **PostgreSQL**: Used in production (Render provides this)
- **python-dateutil**: For date calculations in payment schedules
- **gunicorn**: For running the app on Render
- **whitenoise**: For serving static files (if needed)

# Loan Manager

## Project Structure

```
loan_manager/
├── manage.py
├── loan_manager/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── loan/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── permissions.py
├── user/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   └── authenticate.py
├── requirements.txt
├── runtime.txt
├── Procfile
└── README.md
```


## Local Setup Steps

### 1. Clone the Repository
```bash
git clone <repository_url>
cd loan_manager
```
### 2.Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
Create a .env file in the project root with:
```bash
SECRET_KEY=your_django_secret_key
DEBUG=True  # Set to False in production
DATABASE_URL=sqlite:///db.sqlite3  # For local dev; Render uses PostgreSQL
EMAIL_HOST_USER=your_email@example.com  # Email address for sending OTPs
EMAIL_HOST_PASSWORD=your_email_password  # Email password or app-specific password
ALLOWED_HOSTS=127.0.0.1,localhost  # Comma-separated list for local dev
```
### 5. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```
- **Set role='admin' manually in the database or admin panel.**

### 7. Run Locally
```bash
python manage.py runserver
```
- **Access at http://127.0.0.1:8000/.**


## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

























