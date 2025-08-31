# Project Overview

This directory contains the backend service for the PhysAI application, built using FastAPI. It serves as an API for handling various operations, including user code execution and physics computations. The project leverages `uv` for dependency management and `uvicorn` as the ASGI server. Key technologies include:

*   **FastAPI:** For building the web API.
*   **SQLAlchemy:** For database interactions (implied by `crud.py`, `models.py`, `schemas.py`, and `sql_app.db` mention in `README.md`).
*   **SymPy & NumPy:** For symbolic mathematics and numerical operations, indicating a focus on scientific or physics-related computations.
*   **Python-Jose:** For handling JSON Web Tokens (JWT), suggesting authentication/authorization features.
*   **Pydantic-Settings:** For managing application settings.

The project structure suggests a typical FastAPI application with modules for CRUD operations, data models, and API schemas, alongside a dedicated `physics_engine` for computational tasks.

# Building and Running

The project uses `uv` for dependency management and `uvicorn` to run the FastAPI application.

1.  **Install `uv`:**
    If you don't have `uv` installed, you can install it via `pipx` (recommended) or `pip`:
    ```bash
    pip install pipx
    pipx install uv
    # Or directly:
    # pip install uv
    ```

2.  **Install Backend Dependencies:**
    Navigate to this `backend` directory and install the Python dependencies:
    ```bash
    uv sync
    ```

3.  **Run the Backend Server:**
    From this `backend` directory, run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`. A `sql_app.db` file (SQLite database) will be created in this directory upon first run.

# Development Conventions

Based on the current files, the project follows standard Python and FastAPI conventions.
*   **Code Structure:** Separation of concerns with `main.py` for the application entry point, `crud.py` for database operations, `models.py` for SQLAlchemy models, and `schemas.py` for Pydantic models.
*   **Dependency Management:** Uses `uv` and `pyproject.toml` for managing project dependencies.
*   **Testing:** (TODO: Investigate testing conventions. No explicit test files found in initial scan.)
*   **Linting/Formatting:** (TODO: Investigate linting and formatting tools/configurations.)

# Testing the Physics Computation Engine Endpoint

To test the `/api/solve_problem` endpoint, you can send a POST request. For example, using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/solve_problem/ \
-H "Content-Type: application/json" \
-d '{ "user_code": "print(1 + 1)", "problem_id": 1 }'
```

(Note: The `problem_id` currently uses a dummy problem for demonstration purposes.)
