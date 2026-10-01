# Copilot Instructions - Subodh's Personal Website

## Project Overview
This is a **Django 6.0 personal academic website** serving as a portfolio for CV, research, teaching, and contact information. Single-app monolithic structure with static content pages and minimal database usage (mostly template-based rendering).

## Architecture & Key Components

### Directory Structure
- **`demo/`** - Django project configuration (settings, URLs, WSGI/ASGI)
- **`myapp/`** - Main application with views, models, and templates
- **`myapp/templates/`** - Base template + page-specific templates (home, cv, research, teaching, contact)
- **`myapp/static/css/`** - Custom CSS (style.css); templates also load Bootstrap 4.3.1 CDN
- **`staticfiles/`** - Collected static files for production (generated via `collectstatic`)

### Request Flow
1. URL routing: `demo/urls.py` includes `myapp/urls.py`
2. Views: Simple function-based views in `myapp/views.py` (one view per page) → render templates
3. Templates: Extend `base.html` with page-specific content blocks
4. Static files: WhiteNoise middleware serves CSS/JS in production with compressed manifest storage

## Development Workflows

### Essential Commands
```bash
# Local development server (HTTP only, not HTTPS)
python manage.py runserver

# Database setup
python manage.py migrate

# Collect static files for production
python manage.py collectstatic --noinput

# Django shell for testing
python manage.py shell
```

### Build Pipeline (Production)
See `build.sh` - runs in order: pip upgrade → requirements install → collectstatic → migrate
- Deploy-compatible (used in Render.com CI/CD)
- Uses `python manage.py collectstatic --noinput` with WhiteNoise compressed manifest

### Important Settings
- **Debug mode** controlled by `DJANGO_DEBUG` env var (default False in production)
- **Secret key** from `DJANGO_SECRET_KEY` env var (fallback to insecure default)
- **Hosts**: localhost, 127.0.0.1, .onrender.com, subodhpandey.com.np
- **Security**: SSL/HSTS enabled when DEBUG=False; disabled in development

## Key Patterns & Conventions

### View Pattern
All views are simple function-based, template-render pattern:
```python
def home(request):
    return render(request, "home.html")
```
**No complex business logic** - add new page views by creating a simple view + template + URL entry.

### Template Structure
- `base.html` contains navbar with Bootstrap 4 + shared structure
- Page templates inherit from base.html and override `title` and content blocks
- Navigation links use Django `{% url %}` template tag (e.g., `{% url 'home' %}`)

### Static Files Handling
- **Development**: Django serves from `myapp/static/` automatically
- **Production**: Must run `collectstatic` to copy to `staticfiles/` before serving
- **Storage backend**: `CompressedManifestStaticFilesStorage` (WhiteNoise) - adds hash to filenames

### Database
- **ORM**: Django ORM with minimal models (e.g., `TodoItem` model exists but may be unused)
- **Migrations**: Auto-generated in `myapp/migrations/`; apply with `manage.py migrate`
- **DB**: SQLite3 (`db.sqlite3`); suitable for portfolio site

## Integration Points & Dependencies

### External Dependencies
- **Django 6.0** - framework
- **WhiteNoise 6.11.0** - static file serving middleware
- **Gunicorn 23.0.0** - production WSGI server
- **Bootstrap 4.3.1** - loaded via CDN in templates

### Middleware Stack (Important)
Order matters:
1. `SecurityMiddleware` → `WhiteNoiseMiddleware` (static files) → Session/Auth/CSRF → Messages
2. WhiteNoise must come after SecurityMiddleware

### HTTPS Note
Django dev server only supports HTTP. If seeing `ERR_SSL_PROTOCOL_ERROR`:
- Use `http://127.0.0.1:8000` (not https)
- Clear browser cache/site data
- Check for HTTPS-forcing browser extensions

## Common Modifications

### Adding a New Page
1. Add view function in `myapp/views.py`: `def newpage(request): return render(request, "newpage.html")`
2. Create template `myapp/templates/newpage.html` extending `base.html`
3. Add URL route in `myapp/urls.py`: `path("newpage/", views.newpage, name="newpage")`
4. Add nav link in `base.html`: `<a href="{% url 'newpage' %}">New Page</a>`

### CSS Modifications
- Edit `myapp/static/css/style.css` for custom styles
- Run `collectstatic` before production deployment
- Bootstrap classes available via CDN in templates

### Static Files in Production
After any static file changes:
```bash
python manage.py collectstatic --noinput
```
This must run before deployment to update the `staticfiles/` directory and hash-based filenames.

## Testing & Validation
- Django admin available at `/admin/` (configure superuser with `createsuperuser`)
- No test suite currently in place; add tests to `myapp/tests.py` following Django conventions
- Run tests with `python manage.py test`
