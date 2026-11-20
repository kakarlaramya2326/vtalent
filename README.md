# VTalent Admissions

## Run locally

From the repository root:

```powershell
.\myvenv\Scripts\python.exe mypro\manage.py migrate
.\myvenv\Scripts\python.exe mypro\manage.py runserver
```

Local runs default to development mode. Install dependencies first with `pip install -r requirements.txt`.

## Deploy to Render

1. Create a persistent PostgreSQL database in Render.
2. Create a Blueprint from this repository and provide that database's **internal** connection URL for `DATABASE_URL` when prompted.
3. Keep `DJANGO_DEBUG` set to `false`. Render generates `DJANGO_SECRET_KEY`; the app automatically trusts the Render hostname and configures HTTPS.

The Blueprint uses the repository root. Its build command installs dependencies and collects static files; its start command applies database migrations and launches Gunicorn. The SQLite database is only a local development fallback; production requires `DATABASE_URL`.
