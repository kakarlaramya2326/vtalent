# VTalent Admissions

## Run locally

From the repository root:

```powershell
.\myvenv\Scripts\python.exe mypro\manage.py migrate
.\myvenv\Scripts\python.exe mypro\manage.py runserver
```

Local runs default to development mode. Install dependencies first with `pip install -r requirements.txt`.

## Deploy to Render

1. Create a Blueprint from this repository, or update your existing Web Service's build and start commands to match `render.yaml`.
2. Keep `DJANGO_DEBUG` set to `false`. Render generates `DJANGO_SECRET_KEY`; the app automatically trusts the Render hostname and configures HTTPS.
3. This setup enables temporary SQLite with `DJANGO_ALLOW_SQLITE=true` so the site can start without a separate database. SQLite data, including sessions, is not persistent across Render instance replacements. For persistent data, create Render PostgreSQL, set `DATABASE_URL` to its **internal** connection URL, and remove `DJANGO_ALLOW_SQLITE`.

The Blueprint uses the repository root. Its build command installs dependencies and collects static files; its start command applies database migrations and launches Gunicorn.
