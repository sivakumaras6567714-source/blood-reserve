# Blood Donor Emergency Directory

A beginner-friendly full-stack starter using **React + Django REST Framework + Supabase-compatible PostgreSQL**.
It runs immediately with SQLite for local development. You can switch to Supabase PostgreSQL by setting `DATABASE_URL`.

## Requirements
- Python 3.10+
- Node.js 18+
- npm

## 1. Run the backend
Open a terminal in this folder:

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Backend: http://127.0.0.1:8000  
API: http://127.0.0.1:8000/api/

## 2. Run the frontend
Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (usually http://localhost:5173).

## Demo data
The seed command creates sample donors and blood groups. These are fictional demo records.
Use the app's registration form to add more donors and the emergency form to submit requests.

## Supabase setup (optional)
The app uses SQLite by default so it is easy to run locally. To use Supabase:
1. Create a Supabase project.
2. In Supabase, open **Project Settings → Database** and copy the PostgreSQL connection string.
3. In `backend/.env`, set `DATABASE_URL` to that connection string. Use the pooler/direct connection details recommended by Supabase for your environment.
4. Install dependencies and run `python manage.py migrate` again.

Example `backend/.env`:
```env
DJANGO_SECRET_KEY=replace-this-with-a-long-random-secret
DEBUG=True
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT.supabase.co:5432/postgres
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

Do not commit real passwords, API keys, or donor data to source control.

## Important safety and privacy notes
- The directory never returns donor phone numbers or email addresses in public search results.
- The demo contact action records a contact request; it does not expose a donor's private contact details.
- This is an educational prototype, not a verified medical service. Confirm donor identity, local eligibility rules, blood compatibility, and clinical suitability with a qualified healthcare professional.
- The 90-day rule is implemented as the requested project guard. Actual donation eligibility depends on local regulations and medical assessment; the app must not make clinical decisions.
- Before real deployment, add proper authentication, role-based authorization, audit logs, rate limiting, HTTPS, consent flows, data retention rules, and hospital verification review.

## Main API endpoints
- `GET /api/blood-groups/`
- `GET /api/donors/?blood_group=A%2B&location=Coimbatore`
- `POST /api/donors/`
- `POST /api/emergency-requests/`
- `POST /api/contact-requests/`
- `GET /api/health/`

## Project structure
```text
backend/
  config/              Django project settings
  directory/           Models, serializers, API views, management command
frontend/
  src/                 React app and styles
```
