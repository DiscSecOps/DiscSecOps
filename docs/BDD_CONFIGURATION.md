```
project_root/
├── docs/
│   └── features/                 # Gherkin files live here (Source of Truth)
├── frontend/
│   ├── package.json
│   └── tests/
│       └── unit/                 # Vitest JS unit tests stay here
└── backend/
    ├── pyproject.toml            # Pytest config lives here
    ├── my_app/                   # FastAPI & backend code
    └── tests/
        ├── unit/                 # Backend pytest unit tests
        ├── integration/          # Backend API tests
        └── e2e/                  # MOVING HERE: Python Playwright + BDD tests
            ├── conftest.py
            └── step_defs/
```

# pyproject.toml Configuration for pytest   
``` toml
[tool.pytest.ini_options]
# 1. Tell pytest to handle async tests automatically (for our DB fixtures)
asyncio_mode = "auto"

# 2. Tell pytest exactly where to look for test files
# It will look in backend/tests/ (since pyproject.toml is in /backend)
testpaths = [
    "tests",
]

# 3. Tell pytest-bdd where the features folder is
# Because pyproject.toml is in /backend, we go up one level (..) to the root, then into docs
bdd_features_base_dir = "../docs/features"

# Optional but recommended: add CLI flags you always want to run
# e.g., -v for verbose, --strict-markers to avoid typo'd tags
addopts = "-v --strict-markers"

# Register our custom Gherkin tags so pytest doesn't throw warnings
markers = [
    "smoke: Mark a test as a smoke test",
    "critical: Mark a test as critical path",
    "security: Mark a test as a security/RBAC test",
    "complex: Mark tests with complex state management"
]
```


# conftest.py
Here is the complete conftest.py tailored for your /backend/tests/e2e/ directory.

This file acts as the "control center" for your E2E tests. It automatically handles the Playwright browser setup, configures the base URL for your React frontend, and sets up the async connection to your Postgres container so you can securely teleport data into the database before the browser even opens.

``` python
import os
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Import your FastAPI app's Base and Models (adjust paths to match your project)
# from my_app.database import Base
# from my_app.models import User
# from my_app.core.security import get_password_hash

# ==========================================
# 1. PLAYWRIGHT CONFIGURATION
# ==========================================

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configures Playwright. 
    Setting the base_url means your step definitions can just use:
    page.goto("/login") instead of page.goto("http://localhost:3000/login")
    """
    return {
        **browser_context_args,
        "base_url": os.getenv("FRONTEND_URL", "http://localhost:3000"),
        "viewport": {"width": 1280, "height": 720},
    }

# ==========================================
# 2. ASYNC DATABASE CONFIGURATION
# ==========================================

# Point this to your local Docker Postgres container
# Note the '+asyncpg' which is required for async SQLAlchemy
DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", 
    "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"
)

@pytest.fixture(scope="session")
def event_loop():
    """
    Forces pytest to use a single async event loop for the whole test session.
    This is required so our DB engine doesn't close prematurely.
    """
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def async_engine():
    """Creates the SQLAlchemy async engine once per test run."""
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    # Optional: If you need pytest to build your tables on startup:
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)
        
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(async_engine):
    """
    The Magic Fixture: Gives each test a clean database transaction,
    then ROLLS IT BACK when the test finishes. No cleanup needed!
    """
    async with async_engine.connect() as connection:
        transaction = await connection.begin()
        
        async_session_maker = sessionmaker(
            connection, class_=AsyncSession, expire_on_commit=False
        )
        session = async_session_maker()

        yield session  # This is where the test runs

        # Test is over. Close session and rollback everything.
        await session.close()
        await transaction.rollback()

# ==========================================
# 3. HELPER FIXTURES (Data Injection)
# ==========================================

@pytest_asyncio.fixture
async def create_test_user(db_session):
    """
    A factory fixture to instantly teleport a user into Postgres
    before Playwright tries to log them in.
    """
    async def _create_user(username: str, plain_password: str, role: str = "User"):
        # hashed_pw = get_password_hash(plain_password)
        # new_user = User(
        #     username=username, 
        #     hashed_password=hashed_pw,
        #     global_role=role
        # )
        # db_session.add(new_user)
        # await db_session.commit()
        # await db_session.refresh(new_user)
        # return new_user
        pass # Replace with actual SQLAlchemy model logic above
        
    return _create_user
```    

# Code generation

pytest-bdd has a built-in code generator, and it is incredibly useful for speeding up your workflow. It analyzes your Gherkin .feature files and automatically writes the Python boilerplate (the @given, @when, @then decorators, and function signatures) for any steps that don't exist yet.

Here are the two ways pytest-bdd handles this for you:

## Method 1: The pytest-bdd generate Command (Best for New Files)

If you just wrote a brand new feature file (like your circle-role.feature) and want to generate the entire Python skeleton in one go, you use the CLI tool.

From inside your /backend directory, run this command:

``` bash
uv run pytest-bdd generate ../docs/features/[my-feature].feature
``` 
e.g.
``` bash
uv run pytest-bdd generate ../docs/features/circle-role.feature
```

What happens:
It will output the complete Python skeleton directly to your terminal screen. It is smart enough to use parsers.parse for variables it detects in your strings!

The output will look exactly like this:

``` Python
from pytest_bdd import given, when, then, parsers

@given(parsers.parse('I am logged in as {username}'))
def _(username):
    raise NotImplementedError

@when(parsers.parse('I view the circle settings'))
def _():
    raise NotImplementedErrors

@then(parsers.parse('I should see "{badge_text}" badge'))
def _(badge_text):
    raise NotImplementedError
```

Tip: You can route this output directly into a new Python file so you don't even have to copy-paste:
``` bash

uv run pytest-bdd generate ../docs/features/circle-role.feature > tests/e2e/step_defs/test_roles.py
```
(Then you just open test_roles.py, rename the _ functions to something descriptive, and add your Playwright/Database logic!)

## Method 2: Test Failure Output (Best for Adding a Single Step)

If you already have your tests running, but a Product Manager adds one new step to an existing scenario in your feature file, you don't need to regenerate the whole file.

Just run your standard test command:
``` bash

pytest tests/e2e/step_defs/
```
What happens:
Pytest will immediately fail the test and print a StepDefinitionNotFoundError. Right inside the error message, it will give you the exact code snippet you need to copy and paste to fix it:

``` Plaintext

E       pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: 
E       Given "I click the advanced settings button". 
E       
E       You can implement it with:
E       
E       @given(parsers.parse('I click the advanced settings button'))
E       def _():
E           raise NotImplementedError

```

# Database stratgey for testing

Unifying your testing strategy now, before you write dozens of tests, will save your team many hours of refactoring later.

I see that your existing API tests currently use an in-memory SQLite database (sqlite+aiosqlite:///:memory:). It also overrides the FastAPI get_db dependency so your application uses this test database during API calls.

To achieve your goals of consistency and reusability, we need to unify the API tests and the new BDD tests to use the exact same database engine and fixtures.

Here is the strategy to align everything.


1. The Database Strategy: Postgres vs. SQLite

The Recommendation: Stop using SQLite for tests and use a dedicated Postgres test database for everything.

While SQLite is fast, it does not perfectly match Postgres. Things like JSONB columns, specific asyncpg behaviors, or advanced SQLAlchemy features might work in tests but fail in production (or vice versa). Since you are using Docker, spinning up a real Postgres database specifically for tests is easy and ensures 100% parity with production.

2. Updating compose.yml

Yes, you should define a test database in your Compose file! Sharing your app_db with your tests is dangerous because the test suite will constantly delete and recreate tables, wiping out the data you use for manual development.

Add this service to your compose.yml. Note the use of tmpfs—this runs the Postgres database entirely in your computer's RAM, making it nearly as fast as in-memory SQLite!
YAML

  # Add this right below your existing 'db' service
  test_db:
    image: postgres:16-alpine
    restart: unless-stopped
    # Use tmpfs to keep the DB in memory for blazing fast tests!
    tmpfs:
      - /var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: test_db
    ports:
      - "5434:5432" # Exposed on a different port so it doesn't clash with dev DB

3. Handling Alembic

For testing, you have two choices for creating your tables:

    Alembic Upgrades: Run alembic upgrade head programmatically at the start of your tests. This is the most "pure" approach.

    SQLAlchemy create_all: Let SQLAlchemy create the tables based on your models. This is what your current SQLite test does.

Recommendation: Stick with Base.metadata.create_all for your test suite. It is significantly faster than running dozens of Alembic migration files every time you run pytest. We will use this in our unified configuration.

4. The Unified /backend/tests/conftest.py

To make your code reusable, we will move the database and client fixtures out of test_auth.py and into a single conftest.py file located at /backend/tests/conftest.py.

Because it is at the root of the tests folder, both your API tests (/tests/unit) and your BDD tests (/tests/e2e) will share the exact same setup!





# Playwright Code Generator

With the Playwright Code Generator you do not have to guess the page.get_by_role(...) commands.
If for example, if you are unsure how to select the "Settings" button in your React app, you can run the following command in your terminal:
``` bash
playwright codegen http://localhost:3000 
```
***This opens up a browser window on the dev container itself, not your own PC. To access this browser window, we go in via the VNC service configured on port 6080:***

**http://localhost:6080**

Once you are in via VNC, you can then navigate the app, click, perform actions like entering data in a field etc. These actions are then recorded as python code in a separate Playwright Inspector window (within the VNC session). 
Now you can copy the exact Python code it generates to use in your step definitions.





# Actions taken
- Added test_db container
- Added backend/tests/conftest.py
- Moved config from /backend/tests/test_auth.py to backend/tests/conftest.py so it can be shared
- Created folder /backend/tests/e2e
- Created folder /backend/tests/integration
- Moved backend/tests/test_auth.py to /backend/tests/integration folder
- Installed pytest-bdd package and dependencies via uv package manager
- Installed VS Code extension "Cucumber (Gherkin) Full Support"
- Added TEST_DATABASE_URL to .env file in ci-cd.yml #TODO: do we still need the DATABASE_URL parameter in CI?


- Changed Makefile command test-e2e to run pytest playwright tests
- Updated Playwright container version in Dockerfile
- Configured backend/tests/e2e/step_defs/test_ui.py for testing docs/features/ui/feature
- Added create_test_user fixture to conftest.py
- TODO: remove playwright and related sependencies from npm