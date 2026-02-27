# 📖 Full-Stack BDD Testing Playbook

This document defines the architecture and workflow for Behavior-Driven Development (BDD) using Pytest-BDD, Playwright, and FastAPI.

## The Big Picture (How Everything Connects)

Here is a mental model of how the entire BDD testing architecture fits together.

Think of the process as a relay race with 4 main stages:

### Stage 1: The Blueprint (Product & Docs)

- **Where**: /docs/features/circle-role.feature
- **What**: You write plain English rules.
- **Purpose**: To define what the system should do in a way anyone (developers, managers, QA) can read.

### Stage 2: The Translation (Step Definitions)

- **Where**: /backend/tests/e2e/step_defs/test_roles.py
- **What**: This is the Python file that links the English sentences to Python functions.
- **Purpose**: It acts as a translator. When pytest reads Given I log in, this file says, "Ah, I have a Python function for that!"

### Stage 3: The Helpers (Fixtures & Setup)

- **Where**: /backend/tests/e2e/conftest.py
- **What**: The invisible setup crew.
- **Purpose**: Before your test even clicks a button, this file starts the Playwright browser and connects to your Postgres database. It hands the page (browser) and db_session (database) to your Stage 2 functions so they can do their jobs.

### Stage 4: Execution (Running the Test)

When you type pytest in your terminal, here is the exact chronological order of what happens:

- Pytest starts up: It finds your conftest.py and gets the database and browser ready.
- Reads the Feature: It opens /docs/features/circle-role.feature and reads the first line: Given I am logged in as alice.
- Finds the Match: It searches /tests/e2e/step_defs/ and finds the Python function decorated with @given('I am logged in as alice').
- Runs the Code: It executes that Python function. Inside that function, Playwright takes over, opens the React app, types "alice", and clicks Login.
- Checks Assertions: It reads Then I should see "👑 Owner" badge. It runs the matching Python code: expect(page.get_by_text("👑 Owner")).to_be_visible().
- Cleanup: Once the scenario finishes, conftest.py steps back in, closes the browser, and rolls back the database so the next test has a totally clean slate.

## 🏗️ Project Architecture

We maintain a strict separation between English specifications, backend logic, and frontend UI.
```Plaintext

project_root/
│
├── docs/
│   └── features/                 # Gherkin .feature files (Source of Truth)
│
├── frontend/                     # React Frontend
│   └── tests/
│       └── unit/                 # Vitest JS unit tests stay here
│
└── backend/                      # FastAPI Backend
    ├── pyproject.toml            # Pytest & Tooling config
    └── tests/
        ├── unit/                 # Backend pytest unit tests
        ├── integration/          # API-level tests (formerly test_auth.py)
        └── e2e/                  # BDD / Playwright tests
        │   └── step_defs/        # Python implementations of Gherkin steps
        ├── conftest.py       # Global fixtures (DB & Browser)
```


## 🛠️ The Database Strategy

To ensure 100% parity with production, we use Postgres for all tests instead of SQLite.

 - Isolation: A dedicated test_db container runs on port 5434 to avoid wiping your development data.
 - Performance: The test database uses tmpfs (RAM storage) for near-instant execution.
 - Schema: We use Base.metadata.create_all for speed in tests, bypassing the need to run heavy Alembic migrations every time.

## 🚀 Workflow: How to Write a Test

### 1. Define Behavior

Write your scenario in plain English in /docs/features/[feature-name].feature.

### 2. Generate Python "Skeleton Code"

From the /backend directory, run the uv generator to create your step definition skeleton:

```Bash
# Generate to terminal
uv run pytest-bdd generate ../docs/features/[my-feature].feature
```
#### OR generate directly to a new file
``` bash
# generate directly to a new file
uv run pytest-bdd generate ../docs/features/[my-feature].feature > tests/e2e/step_defs/test_[name].py
```

### 3. Write the implementation code

The generated code simply generates the elements must exist in the step_def python file, but they are empty. The next job is to write the actual code to make the tests work.

#### Tips for Playwright tests: Don't guess selectors. 
Use the Playwright Generator via our VNC service:

 - Run uv run playwright codegen http://localhost:3000 inside your dev container.
 - Open http://localhost:6080 in your local browser to access the VNC session.
 - Perform actions in the VNC browser; copy the generated Python code from the Inspector window.


## 🧪 Running Tests

We use a unified conftest.py that provides global fixtures for integration, API and E2E tests.

### Makefile commands
``` plaintext
Command                 Purpose

make run-backend-test   Start FastAPI server connected to TEST database (used for E2E tests)
make test-backend	    Runs fast unit and integration tests (ignores E2E).
make test-e2e	        Runs BDD tests headlessly (Standard).
make test-e2e-headed	Runs BDD tests visibly in the VNC window (Port 6080).
```

#### Running integration tests

Simply run the make test-backend command from the project root
``` bash
make test-backend
```

#### Running e2e tests non-headed

Run the following commands:
``` bash
make run-backend-test
make run-frontend
make test-e2e
```

#### Running e2e tests Headed (i.e. visible in the browser)

Run the following commands:
``` bash
make run-backend-test
make run-frontend
make test-e2e
```
Now, open the VNC session in your browser to connect to the headed session running on the dev container:

http://localhost:6080/


## ⚙️ Configuration Reference

### Database Fixtures (conftest.py)

Our db_session fixture uses a transactional rollback strategy:

 - A transaction is opened before the test starts.
 - The test (or Playwright) interacts with the DB.
 - The transaction is rolled back automatically after the test, leaving the DB perfectly clean.

### Environment Variables

 - DATABASE_URL: Used by the FastAPI app in CI to serve the API.
 -  TEST_DATABASE_URL: Used by Pytest to inject test data directly into Postgres.

 ## Simple example

 The **ui.feature** file was used as an example, and the complete step def file for this test is **/backend/tests/e2e/step_defs/test_ui.py**


## ✅ Migration Status & Actions Taken

    [x] Added test_db container with tmpfs optimization.
    [x] Added TEST_DATABASE_URL to .env file in ci-cd.yml
    [x] Installed pytest-bdd package and dependencies via uv package manager
    [x] Installed VS Code extension "Cucumber (Gherkin) Full Support"
    [x] Unified conftest.py created at /backend/tests/.
    [x] Moved test_auth.py to /integration folder.
    [x] Configured pytest-bdd markers and feature paths in pyproject.toml.
    [x] Implemented Playwright browser caching in GitHub Actions.
    [ ] TODO: Remove legacy Playwright/NPM dependencies from frontend/package.json.