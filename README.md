# 🧠 FinanceAI Backend (Django REST Framework)

This is the backend of the **FinanceAI** project, built with Django and Django REST Framework. It powers APIs for managing transactions and handles Firebase Authentication integration.

---

## 🚀 Tech Stack

- Django 5.1.6
- Django REST Framework
- PostgreSQL
- Firebase Admin SDK
- Docker
- CORS / Filters / Logging

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/payallenka/financeAiBackend.git
cd financeAiBackend
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=financeai
DB_USER=your_postgres_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=http://localhost:3001
CORS_ALLOW_CREDENTIALS=True
```

### 5. Export Firebase credentials

Make sure you have your Firebase Admin SDK JSON file (e.g., `financeai-dfe7c-firebase-adminsdk-fbsvc-d1e2e0db3c.json`) in the root directory.

Then run:

```bash
export FIREBASE_CREDENTIALS="$(jq -c . < financeai-dfe7c-firebase-adminsdk-fbsvc-d1e2e0db3c.json)"
```

### 6. Start PostgreSQL via Docker (optional)

```bash
docker start postgres_container
# OR (first-time setup)
docker run --name postgres_container \
  -e POSTGRES_USER=your_user \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=financeai \
  -p 5432:5432 \
  -d postgres
```

### 7. Apply migrations and run the server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 🐛 Debugging

Django logs are written to `django_debug.log`. You can check logs there for authentication or API issues.

---

## ✅ API Base URL

```http
http://localhost:8000/api/
```

---

## 📁 Directory Overview

- `transactions/`: App for handling finance transactions
- `middleware/`: Custom Firebase authentication middleware
- `settings.py`: Environment-aware configuration

---

## 🛡️ Security Notes

- Ensure `.env` and Firebase credentials are **never committed** to version control
- Always use strong secrets and turn off `DEBUG` in production

---

## 📜 License

MIT License © 2025 Payal Lenka
