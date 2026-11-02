# Guided learning: working application and exercises

## What this PR changes
This feature branch contains **working code in the existing Vue / Django folders**. The separate exercise scaffolding lives under `learning-exercises/`. The old `workbook.md` is retained. Product data is fictional. This project has **no database, payment gateway, accounts or automatic order placement**.

## Local setup (PowerShell)
Install Python 3.12, Node.js 22+, Poetry and Git.

```powershell
git clone https://github.com/yenyee160-web/firework-catalogue.git
cd firework-catalogue
git checkout feature/fireworks-learning-platform
py -3.12 -m pip install "poetry>=2,<3"
poetry install
poetry run playwright install chromium
cd frontend
npm ci
npm run dev
```
In another terminal from the repo root:

```powershell
$env:WHATSAPP_NUMBER="60123456789" # Replace with your own authorized business number
$env:DJANGO_DEBUG="1"
poetry run python backend/manage.py runserver
```
Open http://127.0.0.1:5173. The frontend proxies requests to port 8000.

## Production-style local build
```powershell
npm run build --prefix frontend
$env:WHATSAPP_NUMBER="60123456789"
$env:DJANGO_SECRET_KEY="replace-with-a-unique-random-secret"
$env:DJANGO_ALLOWED_HOSTS="your-domain.example"
$env:DJANGO_DEBUG="0"
poetry run python backend/manage.py runserver 127.0.0.1:8000 --noreload
```
Use a real production WSGI server such as Gunicorn on Linux instead of Django runserver for deployment. Put TLS/HTTPS in front of it. `python backend/manage.py check --deploy` is a useful additional security check.

## Environment matrix
| TEST_ENV | BASE_URL | Purpose | Tests |
| --- | --- | --- | --- |
| local | http://127.0.0.1:5173 | Developer workstation | All |
| ci | http://127.0.0.1:8000 | GitHub Actions/Jenkins | All |
| staging | https://staging.example.com | Deployed nonproduction | All; use test contact |
| production | https://your-domain.example | Live site | Smoke only |

`TEST_ENV=production` automatically skips non-smoke tests. Do not run destructive or customer-facing tests against production. This is **not** a safety authorization for initiating real enquiries.

## Run tests and preserve artifacts
```powershell
$env:TEST_ENV="local"
$env:BASE_URL="http://127.0.0.1:5173"
poetry run pytest tests/api tests/unit
New-Item -ItemType Directory -Force artifacts | Out-Null
poetry run pytest tests/e2e --browser chromium --tracing on --video on --screenshot only-on-failure --output artifacts/playwright --junitxml=artifacts/junit.xml --html=artifacts/report.html --self-contained-html
poetry run playwright show-trace artifacts/playwright/<test-name>/trace.zip
```
Videos (WebM), Playwright traces (ZIP), failure screenshots (PNG), JUnit XML and HTML reports are created by pytest-playwright / pytest-html. Artifacts are uploaded even when CI tests fail. Do not commit generated media to Git.

## Git exercises
```powershell
git switch -c exercise/search-improvement
git status
git add learning-exercises
git commit -m "practice: improve search exercise"
git push -u origin exercise/search-improvement
```
Compare branches, open your own PR, request a review, inspect Actions logs, fix a failing check, and squash-merge after approval. Never store WhatsApp contacts or Django secrets in source code.

## Poetry explained
Poetry manages the Python virtual environment and dependency groups via `pyproject.toml`. `poetry install` installs application and developer dependencies; `poetry run pytest` executes tests inside that environment. In a real deployment, commit a generated `poetry.lock` for reproducibility (the PR doesn't contain one because dependencies could not be resolved in this environment).

## Limitations
No online checkout is completed. A constructed WhatsApp link never proves sending or payment. Verify prices and customer eligibility manually. Catalogue changes require editing JSON and redeploying. Before public sale, confirm applicable rules, licenses, age restrictions, shipping restrictions and hosting policies. Tests on this branch are supplied but must pass in Actions before merging.
