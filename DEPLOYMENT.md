# DevDesk Deployment Guide

This guide covers deploying your Django application to Heroku.

## Prerequisites

- Heroku CLI installed: https://devcenter.heroku.com/articles/heroku-cli
- Git repository pushed to GitHub
- Heroku account created

## Deployment Steps

### 1. Create Heroku App

```bash
heroku create your-app-name
# or just: heroku create (generates random name)
```

### 2. Add Heroku Postgres

```bash
heroku addons:create heroku-postgresql:essential-0
```

This automatically sets the `DATABASE_URL` environment variable.

### 3. Set Required Environment Variables

Set these config vars on Heroku (do NOT add ON_HEROKU to your local .env):

```bash
heroku config:set ON_HEROKU=true
heroku config:set SECRET_KEY=A_SUPER_SECRET_STRING_NO_ONE_WILL_EVER_GUESS_OR_KNOW
```

**Important Notes:**
- `ON_HEROKU=true` triggers production settings (PostgreSQL, DEBUG=False, etc.)
- Use a different SECRET_KEY for production than your local dev key
- Do NOT add `ON_HEROKU` to your local `.env` file
- `DATABASE_URL` is automatically provided by the Postgres add-on

### 4. Deploy to Heroku

```bash
git push heroku main
```

### 5. Run Initial Migrations

```bash
heroku run python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
heroku run python manage.py createsuperuser
```

### 7. Collect Static Files

Static files are collected automatically during deployment via the `collectstatic` command in your release phase. If needed manually:

```bash
heroku run python manage.py collectstatic --noinput
```

## Verify Deployment

```bash
# Open your app
heroku open

# View logs
heroku logs --tail

# Check config vars
heroku config
```

## Environment Variables Summary

### Required on Heroku:
- `ON_HEROKU=true` - Enables production mode
- `SECRET_KEY` - Your Django secret key (generate a unique one for production)
- `DATABASE_URL` - Auto-set by Heroku Postgres add-on

### Local .env (Development):
- `SECRET_KEY` - Your local dev secret key
- **DO NOT** include `ON_HEROKU` in your local `.env`

## Troubleshooting

### View Application Logs
```bash
heroku logs --tail
```

### Run Django Shell
```bash
heroku run python manage.py shell
```

### Check Database Connection
```bash
heroku pg:info
```

### Restart App
```bash
heroku restart
```

## Useful Commands

```bash
# Scale web dynos
heroku ps:scale web=1

# Run management commands
heroku run python manage.py <command>

# Access database
heroku pg:psql

# View release history
heroku releases

# Rollback to previous release
heroku rollback
```

## Production Checklist

- [ ] Set unique SECRET_KEY for production
- [ ] Verify ON_HEROKU=true is set
- [ ] Postgres add-on created
- [ ] Migrations run
- [ ] Static files collected
- [ ] Superuser created
- [ ] App opens without errors
- [ ] Check logs for issues

## Additional Configuration (Optional)

### Custom Domain
```bash
heroku domains:add www.yourapp.com
```

### SSL Certificate
Automatic SSL is included on all Heroku apps.

### Email Configuration
For production email, add these to Heroku config:
```bash
heroku config:set EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
heroku config:set EMAIL_HOST=smtp.gmail.com
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USE_TLS=True
heroku config:set EMAIL_HOST_USER=your-email@gmail.com
heroku config:set EMAIL_HOST_PASSWORD=your-app-password
```

## Resources

- Heroku Python Documentation: https://devcenter.heroku.com/categories/python-support
- Django Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
