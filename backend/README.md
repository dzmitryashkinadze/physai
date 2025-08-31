# Backend Service

This directory contains the FastAPI backend service for the PhysAI application.

## Setup and Running

1.  **Install `uv` (if you haven't already):**
    `uv` is a fast Python package installer and resolver. You can install it via `pipx` (recommended) or `pip`:
    ```bash
    pip install pipx
    pipx install uv
    # Or directly:
    # pip install uv
    ```

2.  **Install Backend Dependencies:**
    Navigate to this `backend` directory and install the Python dependencies using `uv`:
    ```bash
    cd backend
    uv sync
    ```

3.  **Run the Backend Server:**
    From this `backend` directory, run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`. A `sql_app.db` file (SQLite database) will be created in this directory upon first run.

## Testing the Physics Computation Engine Endpoint

To test the `/api/solve_problem` endpoint, you can send a POST request. For example, using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/solve_problem/ \
-H "Content-Type: application/json" \
-d '{ "user_code": "print(1 + 1)", "problem_id": 1 }'
```

(Note: The `problem_id` currently uses a dummy problem for demonstration purposes.)
