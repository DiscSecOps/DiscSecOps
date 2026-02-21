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



``` bash
uv run pytest-bdd generate ../docs/features/[my-feature].feature > tests/e2e/step_defs/test[my-test-name].py
``` 
e.g.
``` bash
uv run pytest-bdd generate ../docs/features/circle-role.feature > tests/e2e/step_defs/test_roles.py
```

Method 1: The pytest-bdd generate Command (Best for New Files)

If you just wrote a brand new feature file (like your circle-role.feature) and want to generate the entire Python skeleton in one go, you use the CLI tool.

From inside your /backend directory, run this command:
``` bash
pytest-bdd generate ../docs/features/circle-role.feature
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
    raise NotImplementedError

@then(parsers.parse('I should see "{badge_text}" badge'))
def _(badge_text):
    raise NotImplementedError
```

Tip: You can route this output directly into a new Python file so you don't even have to copy-paste:
``` bash

pytest-bdd generate ../docs/features/circle-role.feature > tests/e2e/step_defs/test_roles.py
```
(Then you just open test_roles.py, rename the _ functions to something descriptive, and add your Playwright/Database logic!)
Method 2: Test Failure Output (Best for Adding a Single Step)

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
