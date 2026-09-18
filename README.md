# Python API Automation Testing Portfolio

A beginner-friendly REST API testing project using **Python, requests, pytest, and pytest-html**. Includes **34 passing test cases**, reusable fixtures, parameterization, HTML reporting, and GitHub Actions.

## Scope

Tests send real HTTP requests to an included local task-management demo API. Requests are not mocked. The server stores tasks in memory and is reset for every test. No external API account, API key, or public service is required. Internet is needed only to install dependencies and publish to GitHub.

This is an educational portfolio, not a production API framework. The server uses a fixed demonstration token and has no database, production authentication, query parameters, pagination, or performance tests. The demo token is not a secret. The client is configured for this local API; remote APIs require their own contract and configuration.

## Features

- GET, POST, PUT, PATCH, and DELETE tests.
- Positive and negative scenarios, including invalid JSON, data types, missing resources, and missing/incorrect authorization.
- Status codes: 200, 201, 204, 400, 401, 404, and 415.
- JSON structure, values, ID type, content type, and empty DELETE body checks.
- Read-after-write persistence checks and checks that rejected updates preserve data.
- Fresh local server and client per test; no test-order dependencies.
- Automatic self-contained HTML report.
- GitHub Actions testing and report artifact upload.

## Quick start: Windows / VS Code

Requires Python 3.12 or newer. Validated on Python 3.12.14.

Extract the ZIP. In VS Code select **File > Open Folder** and open `api-automation-portfolio`. Open **Terminal > New Terminal**:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

No PowerShell activation is required, so these commands avoid the Activate.ps1 execution-policy issue. Use **Python: Select Interpreter** in the command palette and select `.venv\Scripts\python.exe`.

Open `reports/report.html` in a browser. Each run replaces this report. The report has embedded assets and works offline.

## macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest
```

## Run selected tests

Windows examples:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_get.py
.\.venv\Scripts\python.exe -m pytest -k unauthorized
.\.venv\Scripts\python.exe -m pytest tests/test_update.py::test_patch_preserves_other_fields
.\.venv\Scripts\python.exe -m pytest --html=reports/my-report.html --self-contained-html
```

## Structure and suggested reading order

| File | Purpose |
| --- | --- |
| `tests/test_get.py` | Start here: HTTP requests, JSON responses, assertions |
| `api/client.py` | Reusable requests Session, authorization, URL, five-second timeout |
| `conftest.py` | Server, client, payload, and created-task fixtures with cleanup |
| `tests/test_post.py` | Creation, invalid titles/types/JSON/content type |
| `tests/test_update.py` | PUT replacement, PATCH partial update, rejected updates |
| `tests/test_delete.py` | Deletion, absence checks, repeated deletion |
| `tests/test_auth.py` | Missing/incorrect tokens for all five methods |
| `pytest.ini` | Test discovery, import path, automatic HTML report |
| `demo_api/server.py` | Supporting server code; read after the tests |
| `requirements.txt` | Pinned versions of requested dependencies |
| `reports/report.html` | Generated report bundled as an example; ignored by Git |
| `.github/workflows/tests.yml` | CI on push, pull request, or manual trigger |
| `TEST_RESULTS.md` | Actual delivery validation results |

Python package directories also include `__init__.py`. `reports/.gitkeep` preserves the report folder in Git. `.gitignore` excludes virtual environments, Python caches, generated HTML reports, local editor settings, and `.env`.

## API contract

All requests require `Authorization: Bearer demo-token`. The client supplies it. POST, PUT, and PATCH require `Content-Type: application/json`, set automatically by requests when using `json=`.

| Method | Endpoint | Success |
| --- | --- | --- |
| GET | `/tasks` | 200 and JSON array |
| GET | `/tasks/{id}` | 200 and task object |
| POST | `/tasks` | 201 and task with generated integer ID |
| PUT | `/tasks/{id}` | 200 and replacement task |
| PATCH | `/tasks/{id}` | 200 and partially updated task |
| DELETE | `/tasks/{id}` | 204 and empty body |

Example task:

```json
{"id": 1, "title": "Learn API testing", "completed": false}
```

Title must be a non-empty string; whitespace-only titles are rejected. POST and PUT require title. Completed must be a boolean and defaults to false. PUT resets omitted completed to false; PATCH preserves omitted fields. Empty PATCH requests and unknown fields return 400. Invalid JSON or a JSON array returns 400. Missing or incorrect token returns 401 before resource validation. Missing tasks return 404, non-integer IDs return 400, and incorrect content type returns 415.

## Fixtures explained

`api_server` creates a fresh server bound to 127.0.0.1 on an automatically chosen free port. `client` supplies the APIClient. `task_payload` provides reusable valid input. `created_task` creates a task through POST for tests that need existing data. After each test, the client is closed and the server is stopped. Data is discarded, so tests can run independently.

Negative tests should **pass** when invalid requests receive the expected error. There are no intentionally failing tests. The framework stays small so you can study it line by line without abstract base classes or extra validation libraries.

## Publish on GitHub

Create a new empty repository named `api-automation-portfolio`. Do not initialize a README or .gitignore because both are included. Run from the project folder:

```bash
git init
git add .
git commit -m "Add Python API automation portfolio"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/api-automation-portfolio.git
git push -u origin main
```

Replace `YOUR_USERNAME`. If needed, configure Git with your own user.name and user.email before committing. Use GitHub browser authentication when prompted; keep passwords and real tokens out of code.

The project is ready for upload but has not been pushed to your account. GitHub Actions generates a fresh report downloadable from the workflow run's artifacts, even when tests fail. Generated reports are excluded from source control.

Suggested repository description: `Python REST API automation with requests, pytest, fixtures, negative tests, HTML reporting, and GitHub Actions.`

## Troubleshooting

- **No module named pytest/requests:** install requirements with the same virtual-environment Python used to run tests.
- **Activate.ps1 blocked:** use the direct Python commands above; activation is unnecessary.
- **Imports fail:** open and run from the folder containing `pytest.ini`.
- **Local connections blocked:** allow the Python process to use the loopback interface.
- **A test fails:** inspect the traceback and HTML report; fix the cause rather than removing assertions.
