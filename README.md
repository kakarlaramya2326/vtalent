# VTalent Admissions

## Run locally

From the repository root, serve the static site with Python:

```powershell
python -m http.server 8000
```

Open `http://localhost:8000`. The site uses static HTML, CSS, and inline JavaScript; no Python packages, database, or backend server are needed. Registration enquiries are validated in the browser and opened in WhatsApp.

## Folder layout

```text
index.html             Redirects to the homepage
templates/             HTML pages
  index.html            Homepage
  about-ceo.html
  about-institute.html
  contact.html
  courses.html
  internships.html
  student-placements.html
  student-registration.html
static/                Site assets
  css/                  Stylesheets
  images/               Logos and page images
  videos/               Institute video
```

## Publish

Publish the static site from the repository root with any static website host. HTML pages are in `templates/`, and images and stylesheets are in `static/`. No build command, environment variables, or backend are required.
