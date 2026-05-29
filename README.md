# 2lsn

## Deployment on Render.com

This project is configured for deployment on Render.com using a Python web service.

### Required Environment Variables

Set these in Render's Environment tab:
- `SECRET_KEY` - Django secret key for production
- `DEBUG` - Set to `False` (optional, defaults to False)
- `ALLOWED_HOSTS` - Comma-separated hosts (optional, defaults to `.render.com`)

### Automatic Configuration

The `render.yaml` file defines:
- Build command: Installs dependencies and collects static files
- Start command: Runs Gunicorn WSGI server on the provided PORT
