# VTalent Admissions

## Run locally

From the repository root:

```powershell
.\myvenv\Scripts\python.exe mypro\manage.py runserver
```

Local runs default to debug mode and a development-only secret when no Render hostname is present. In production, set `DJANGO_DEBUG=false` and provide `DJANGO_SECRET_KEY`. Install dependencies first with `pip install -r requirements.txt`. No migration command or persistent database is needed.

## Deploy to Render

1. Create a Blueprint from this repository, or update your existing Web Service to use the commands below.
2. Set `DJANGO_SECRET_KEY` to a secure secret and `DJANGO_DEBUG` to `false`. The Blueprint generates the secret automatically.
3. The site uses in-memory SQLite only for Django's default database connection; it does not persist data or require an external database. Student registration is sent directly to WhatsApp and is not saved by the site.
4. The `vtalent.in`, `www.vtalent.in`, and Render hostnames are allowed automatically. Configure the custom domain in Render and point its DNS records to the values Render provides.
5. If configuring the service in the Render Dashboard, use the repository root as its root directory. The build must run `collectstatic` successfully before Gunicorn starts; otherwise WhiteNoise's manifest storage can raise a server error while rendering templates.

Build command:

```sh
pip install -r requirements.txt && python mypro/manage.py collectstatic --noinput
```

Start command:

```sh
gunicorn --chdir mypro mypro.wsgi:application --bind 0.0.0.0:$PORT
```
