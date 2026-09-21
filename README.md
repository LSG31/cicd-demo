# Automated CI/CD Pipeline — Python + Docker + GitHub Actions

A production-style starter project demonstrating:

**GitHub → Build → Test → Docker → Deploy → Monitor**

## Architecture

1. Developer pushes code to GitHub.
2. GitHub Actions installs dependencies and runs pytest on Python 3.11 and 3.12.
3. A Docker image is built and smoke-tested.
4. On `main`, the image is published to GitHub Container Registry (GHCR).
5. GitHub Actions deploys the image to a staging server over SSH.
6. Production deployment is available as a manual workflow after staging succeeds.
7. The app exposes `/health`, `/ready`, and `/info`; Docker health checks and container logs provide basic observability.

## Run locally

### Option A: Python

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python -m app.main
```

Open http://localhost:8000/health

### Option B: Docker Compose

```bash
docker compose up --build -d
curl http://localhost:8000/health
```

View logs:

```bash
docker compose logs -f app
```

Stop:

```bash
docker compose down
```

## GitHub setup

1. Create a new GitHub repository.
2. Push this project to it.
3. In **Settings → Actions → General**, allow GitHub Actions and read/write package permissions as needed. The workflow uses the built-in `GITHUB_TOKEN` to publish to GHCR.
4. In **Settings → Environments**, create `staging` and `production`.
5. Add these environment secrets to each environment:
   - `DEPLOY_HOST` — server IP/hostname
   - `DEPLOY_USER` — SSH user
   - `DEPLOY_SSH_KEY` — private SSH key used by GitHub Actions
6. On the target Linux server, install Docker and make sure the SSH user can run Docker.
7. Make the GHCR package accessible to the server. For a private image, authenticate Docker on the server to GHCR with a read-only package token.

### Deployment flow

- Push to `main` → test → build → push image → deploy staging.
- Use **Run workflow** with `production` → deploy production after staging succeeds.

## Monitoring / observability

This starter keeps monitoring intentionally simple:

- `/health`: liveness/health endpoint.
- `/ready`: readiness endpoint.
- `/info`: environment, version and uptime.
- Docker `HEALTHCHECK`: automatic container health status.
- Gunicorn stdout/stderr: application/server logs.
- `docker logs`: basic log access.

For a larger system, the next step would be Prometheus + Grafana for metrics, and Loki/ELK/OpenSearch for centralized logs.

## Environment management

The same image is promoted between environments; configuration is supplied at runtime with environment variables. GitHub Environments provide separate deployment controls and secrets for staging and production.

## Important security note

Never commit passwords, SSH private keys, API tokens, or `.env` files containing secrets. Use GitHub Secrets/Environments or a dedicated secrets manager.
