# Python API Automation Testing Portfolio

A beginner-friendly REST API automation testing project built with **Python, requests, pytest, and pytest-html**.

The project contains **34 passing automated API tests**, reusable fixtures, positive and negative scenarios, HTML reporting, and GitHub Actions CI.

## Project Scope

Tests send real HTTP requests to an included local task-management demo API. Requests are not mocked.

The local API server stores tasks in memory and is reset for every test, allowing tests to run independently without relying on test execution order.

No external API account, API key, or public service is required.

This project is designed as an educational QA Automation portfolio project rather than a production API framework.

## Technologies

* Python
* requests
* pytest
* pytest-html
* Git
* GitHub
* GitHub Actions

## Test Coverage

The project includes automated tests for:

* GET
* POST
* PUT
* PATCH
* DELETE
* Authentication
* Positive scenarios
* Negative scenarios
* Invalid JSON
* Invalid data types
* Missing resources
* Missing or incorrect authorization

Tested HTTP status codes include:

* `200 OK`
* `201 Created`
* `204 No Content`
* `400 Bad Request`
* `401 Unauthorized`
* `404 Not Found`
* `415 Unsupported Media Type`

The tests also verify:

* JSON response values
* JSON structure
* Generated ID type
* Content-Type
* Empty DELETE response body
* Data persistence after creation and updates
* Preservation of data after rejected updates

## Project Structure

| File                          | Purpose                                                     |
| ----------------------------- | ----------------------------------------------------------- |
| `tests/test_get.py`           | GET endpoint tests                                          |
| `tests/test_post.py`          | POST and validation tests                                   |
| `tests/test_update.py`        | PUT and PATCH tests                                         |
| `tests/test_delete.py`        | DELETE tests                                                |
| `tests/test_auth.py`          | Authentication tests                                        |
| `api/client.py`               | Reusable API client based on requests                       |
| `conftest.py`                 | pytest fixtures for server, client, payloads, and test data |
| `demo_api/server.py`          | Local demo backend used for testing                         |
| `pytest.ini`                  | pytest configuration and HTML reporting                     |
| `requirements.txt`            | Project dependencies                                        |
| `reports/`                    | Generated HTML test reports                                 |
| `.github/workflows/tests.yml` | GitHub Actions CI workflow                                  |
| `TEST_RESULTS.md`             | Test execution and validation information                   |

Python package directories also contain `__init__.py`.

`reports/.gitkeep` keeps the reports directory in Git even when generated reports are ignored.

## API Contract

All requests require:

```text
Authorization: Bearer demo-token
```

The API client automatically supplies this header.

POST, PUT, and PATCH requests use:

```text
Content-Type: application/json
```

### Endpoints

| Method | Endpoint      | Expected Success                 |
| ------ | ------------- | -------------------------------- |
| GET    | `/tasks`      | `200` and JSON array             |
| GET    | `/tasks/{id}` | `200` and task object            |
| POST   | `/tasks`      | `201` and newly created task     |
| PUT    | `/tasks/{id}` | `200` and replaced task          |
| PATCH  | `/tasks/{id}` | `200` and partially updated task |
| DELETE | `/tasks/{id}` | `204` and empty response body    |

Example task:

```json
{
  "id": 1,
  "title": "Learn API testing",
  "completed": false
}
```

## Fixtures

The project uses pytest fixtures to reduce duplicated setup code.

### `api_server`

Creates a fresh local API server for the test.

The server runs on:

```text
127.0.0.1
```

using an automatically selected free port.

### `client`

Creates an `APIClient` connected to the local server.

### `task_payload`

Provides reusable valid task data.

Example:

```python
{
    "title": "Learn API testing",
    "completed": False
}
```

### `created_task`

Creates a task through the POST endpoint before tests that require an existing resource.

After each test:

* the API client is closed
* the local server is stopped
* task data is discarded

This keeps tests isolated from each other.

## Running the Project

### Windows / VS Code

Python 3.12+ is recommended. The project has also been run successfully with Python 3.14.

Create a virtual environment:

```powershell
py -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Using the virtual-environment Python directly means PowerShell activation is not required.

If `Activate.ps1` is blocked by the Windows execution policy, the commands above still work.

## Running Selected Tests

Run only GET tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_get.py
```

Run only DELETE tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_delete.py
```

Run tests matching a keyword:

```powershell
.\.venv\Scripts\python.exe -m pytest -k unauthorized
```

Run one specific test:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_update.py::test_patch_preserves_other_fields
```

## HTML Report

Generate a self-contained HTML report:

```powershell
.\.venv\Scripts\python.exe -m pytest --html=reports/report.html --self-contained-html
```

Then open:

```text
reports/report.html
```

in a browser.

## GitHub Actions

The project contains a GitHub Actions workflow:

```text
.github/workflows/tests.yml
```

Automated tests can run when code is pushed to GitHub or when a pull request is created.

The workflow can also generate the pytest HTML report as an artifact.

## Negative Testing

Negative tests are expected to **pass** when the API correctly rejects invalid requests.

For example:

```text
DELETE /tasks/999
```

should return:

```text
404 Not Found
```

with:

```json
{
  "error": "Task not found"
}
```

This means the test passes because the API behaved exactly as expected.

There are no intentionally failing tests in this project.

## Repository

GitHub repository:

https://github.com/blas-bb/api-automation-portfolio

## Git Workflow

Typical workflow after changing the project:

```bash
git status
git add .
git commit -m "Describe the change"
git push
```

`git add` selects changes for the next commit.

`git commit` saves a version of those changes in the local Git history.

`git push` sends the commits to GitHub.

## Troubleshooting

**No module named pytest or requests**

Install dependencies using the same Python interpreter that runs the tests:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Activate.ps1 is blocked**

You do not need to activate the virtual environment. Run its Python executable directly.

**Imports fail**

Run pytest from the main project directory containing:

```text
pytest.ini
```

**A test fails**

Check the pytest traceback and HTML report. Fix the cause rather than removing the assertion.

---

This project demonstrates practical REST API automation testing using Python, pytest, reusable fixtures, negative testing, automated reporting, Git, and CI.
