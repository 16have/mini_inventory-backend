# Mini Inventory

This repository deploys as a single Flask service: Flask serves the browser UI
at `/` and exposes the API under `/api`. The production database is PostgreSQL.

## Deploy to Render

1. Commit and push this repository to GitHub, GitLab, or Bitbucket.
2. In Render, select **New** → **Blueprint** and connect the repository.
3. Render detects `render.yaml`. Review the `mini-inventory` web service and
   `mini-inventory-db` PostgreSQL database, then click **Apply**.
4. Wait for the deploy to complete, then open the web service URL. The initial
   migration runs automatically before Gunicorn starts.

`render.yaml` creates `SECRET_KEY` and `JWT_SECRET_KEY` as Render-managed
random values and passes the database connection string as `DATABASE_URL`.
Never commit production secret values to the repository.

## Local development

```bash
pipenv install
pipenv run python run.py
```

Local development uses `instance/inventory.db`. Production uses Render
PostgreSQL whenever `DATABASE_URL` is set.

## Routes

- `GET /` — frontend
- `GET /api/health` — deployment health check
- `POST /api/auth/signup`
- `POST /api/auth/login`
- `GET|POST /api/items`
- `GET /api/dashboard`

All inventory and dashboard requests require an `Authorization: Bearer <token>`
header. The included frontend handles this after sign-in.
