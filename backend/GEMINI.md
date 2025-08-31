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
    Navigate to this `backend` directory and install the Python dependencies using `uv`:
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

# Backend Endpoints Plan

This document outlines the proposed backend endpoints for the PhysAI application, covering data retrieval for the frontend and specific functionalities like equation validation.

## 1. Home Page Data (List All Courses)

*   **Endpoint:** `GET /courses`
*   **Description:** Retrieves a list of all available courses to populate the home page.
*   **Response Body (JSON Array of Course Objects):**
    ```json
    [
        {
            "id": "string",
            "title": "string",
            "logo_url": "string",
            "summary": "string",
            "topic": "string",
            "difficulty": "string"
        }
    ]
    ```

## 2. Course Page Data (Retrieve Single Course with Problems)

*   **Endpoint:** `GET /courses/{course_id}`
*   **Description:** Retrieves detailed information for a specific course, including a list of associated problems.
*   **Path Parameters:**
    *   `course_id`: Unique identifier for the course (e.g., UUID or integer).
*   **Response Body (JSON Object):**
    ```json
    {
        "id": "string",
        "title": "string",
        "logo_url": "string",
        "summary": "string",
        "topic": "string",
        "difficulty": "string",
        "problems": [
            {
                "id": "string",
                "title": "string",
                "tags": ["string"],
                "order": 0
            }
        ]
    }
    ```
*   **Note:** Problems in this list will be sorted by their `order` field in ascending order.

## 3. Problem Solving Page Data (Retrieve Single Problem Details)

*   **Endpoint:** `GET /problems/{problem_id}`
*   **Description:** Retrieves comprehensive details for a specific problem, including its description and solutions.
*   **Path Parameters:**
    *   `problem_id`: Unique identifier for the problem (e.g., UUID or integer).
*   **Response Body (JSON Object):**
    ```json
    {
        "id": "string",
        "title": "string",
        "description": "string",
        "solution_markdown": "string",
        "solution_equation": "string",
        "known_parameters": {
            "parameter_name": "string",
            "unit": "string"
        },
        "variable_to_find": "string",
        "figures": ["string"]
    }
    ```

## 4. Validate System of Equations

*   **Endpoint:** `POST /validate_equations`
*   **Description:** Accepts a system of equations from the user and returns a validation result.
*   **Request Body (JSON Object):**
    ```json
    {
        "equations": [
            "string" 
        ]
    }
    ```
*   **Response Body (JSON Object):**
    ```json
    {
        "is_valid": true,
        "errors": [
            "string"
        ]
    }
    ```

## 5. Search Problems by Topic/Difficulty

*   **Endpoint:** `GET /problems/search`
*   **Description:** Searches for problems based on provided topic and/or difficulty.
*   **Query Parameters:**
    *   `topic`: Optional, `string`. Filters problems by topic.
    *   `difficulty`: Optional, `string`. Filters problems by difficulty.
*   **Response Body (JSON Array of Problem Objects):**
    ```json
    [
        {
            "id": "string",
            "title": "string",
            "tags": ["string"]
        }
    ]
    ```

## Problem Attributes

Each problem will have the following attributes to facilitate categorization and search:

*   **`topic`**: Categorization by physics topic (e.g., "Kinematics", "Electrostatics", "Thermodynamics", "Quantum Mechanics").
*   **`difficulty`**: Indication of the problem's complexity or target audience (e.g., "School Grade", "University", "Advanced Research").

*   **`required_concepts`**: A list of fundamental physical equations or concepts necessary to solve the problem (e.g., "Newton's Second Law", "Conservation of Energy", "Maxwell's Equations", "Ohm's Law", "Schrödinger Equation").

# Database Data Model Plan

This document outlines the proposed database schema for the PhysAI application, detailing the relationships between courses, problems, and their associated attributes.

## 1. Course Model

Represents a collection of problems, typically grouped by subject or curriculum.

| Field      | Type     | Description                               |
| :--------- | :------- | :---------------------------------------- |
| `id`       | `UUID`   | Primary Key, unique identifier for the course. |
| `title`    | `String` | The title of the course.                  |
| `summary`  | `Text`   | A brief description or overview of the course. |
| `logo_url` | `String` | URL or path to the course's logo image.   |
| `topic`    | `String` | The primary topic of the course (e.g., "Mechanics", "Electromagnetism"). |
| `difficulty` | `String` | The difficulty level of the course (e.g., "Beginner", "Intermediate", "Advanced"). |

## 2. Problem Model

Represents an individual physics problem.

| Field             | Type     | Description                               |
| :---------------- | :------- | :---------------------------------------- |
| `id`              | `UUID`   | Primary Key, unique identifier for the problem. |
| `title`           | `String` | The title of the problem.                 |
| `description`     | `Text`   | The full text description of the problem. |
| `solution_markdown` | `Text`   | The solution to the problem in Markdown format. |
| `solution_equation` | `Text`   | The solution to the problem as a symbolic equation (e.g., LaTeX or SymPy string). |
| `known_parameters`  | `JSON`   | A JSON object representing known parameters (e.g., `{"w": {"unit": "N"}}`). If native JSON type is not supported by DB, use `Text` to store JSON string. |
| `variable_to_find`  | `String` | The variable that needs to be found in the problem. |
| `difficulty`      | `String` | The difficulty level of the problem (e.g., "School Grade", "University", "Advanced Research"). |
| `figures`         | `JSON`   | A JSON array of URLs or paths to associated figures (e.g., `["url1", "url2"]`). |
| `order`           | `Integer`| The display order of the problem within its course. |
| `course_id`       | `UUID`   | Foreign Key referencing the `Course` model. |


## 4. Topic Model

Categorizes problems by their physics topic.

| Field    | Type     | Description                               |
| :------- | :------- | :---------------------------------------- |
| `id`     | `UUID`   | Primary Key, unique identifier for the topic. |
| `name`   | `String` | The name of the physics topic (e.g., "Kinematics", "Electrostatics", "Thermodynamics"). |

## 5. PhysicsLaw Model

Represents fundamental physical laws or concepts applicable to problems.

| Field    | Type     | Description                               |
| :------- | :------- | :---------------------------------------- |
| `id`     | `UUID`   | Primary Key, unique identifier for the physics law. |
| `name`   | `String` | The name of the physics law or concept (e.g., "Newton's Second Law", "Conservation of Energy", "Ohm's Law"). |
| `equation` | `Text`   | The symbolic representation of the physics law (e.g., LaTeX or SymPy string). |


## 7. Junction Tables (Many-to-Many Relationships)

These tables link problems to multiple difficulties, topics, physics laws, and sources.



### ProblemTopic

Links `Problem` to `Topic`.

| Field        | Type   | Description                               |
| :----------- | :----- | :---------------------------------------- |
| `problem_id` | `UUID` | Foreign Key referencing `Problem.id`.     |
| `topic_id`   | `UUID` | Foreign Key referencing `Topic.id`.       |

### ProblemPhysicsLaw

Links `Problem` to `PhysicsLaw`.

| Field           | Type   | Description                               |
| :----------- | :----- | :---------------------------------------- |
| `problem_id`    | `UUID` | Foreign Key referencing `Problem.id`.     |
| `physics_law_id` | `UUID` | Foreign Key referencing `PhysicsLaw.id`. |

# Software Design Document

This document outlines the key architectural and technological decisions for the PhysAI backend service.

## 1. API Framework

*   **Choice:** FastAPI
*   **Justification:** FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It offers automatic interactive API documentation (Swagger UI and ReDoc), data validation, and serialization out-of-the-box, which significantly speeds up development and ensures robust APIs. Its asynchronous capabilities (ASGI) are well-suited for high-concurrency applications.

## 2. Database

*   **Choice:** SQLite
*   **Justification:** For initial development and prototyping, SQLite is an excellent choice due to its simplicity, file-based nature (no separate server process needed), and ease of setup. It's suitable for small to medium-sized applications or as a local development database.
*   **Future Considerations:** For production environments requiring higher concurrency, scalability, and robust features like replication and advanced backup strategies, a more powerful relational database like PostgreSQL or MySQL would be considered.

## 2.1. Object-Relational Mapper (ORM)

*   **Choice:** SQLAlchemy
*   **Justification:** SQLAlchemy is a powerful and flexible SQL toolkit and Object-Relational Mapper (ORM) for Python. It provides a full suite of well-known enterprise-level persistence patterns, designed for efficient and high-performing database access. It allows developers to interact with databases using Python objects, abstracting away raw SQL queries, while still providing the flexibility to write raw SQL when needed. Its declarative style for defining models integrates well with FastAPI's Pydantic models.

## 3. Database Migrations

*   **Choice:** Alembic
*   **Justification:** Alembic is a lightweight database migration tool for usage with the SQLAlchemy database toolkit. It provides a robust and flexible way to manage database schema changes over time, allowing for version control of the database schema alongside the application code. It supports both "offline" (script-based) and "online" (direct database interaction) migrations.
*   **Alternatives Considered:**
    *   **SQLAlchemy-migrate:** Older and less actively maintained compared to Alembic.
    *   **Raw SQL scripts:** While possible, this approach lacks version control, dependency management, and automation provided by dedicated migration tools.

## 4. Storing and Serving Logos/Figures

*   **Strategy:**
    *   **Storage:** For initial development, figures and logos can be stored directly on the server's file system within a designated static files directory.
    *   **Serving:** FastAPI can serve static files directly. The `logo_url` and `figures` fields in the data model would store the relative paths or URLs to these static assets.
*   **Future Considerations (Scalability & Performance:
    *   **Cloud Object Storage:** For production, storing assets in cloud object storage services like Amazon S3, Google Cloud Storage, or Azure Blob Storage is highly recommended. These services offer high availability, scalability, durability, and cost-effectiveness.
    *   **Content Delivery Networks (CDNs):** Using a CDN (e.g., Cloudflare, Amazon CloudFront) in conjunction with object storage would cache assets globally, reducing latency and improving load times for users worldwide.

## 5. Security Concerns (Initial State)

*   **Authentication/Authorization:** For the initial phase, all endpoints will be accessible without any authentication or authorization. This simplifies development and allows for rapid prototyping.
*   **Future Considerations:**
    *   **User Authentication:** Implement user authentication (e.g., OAuth2, JWT) for protected endpoints.
    *   **Role-Based Access Control (RBAC):** Define roles and permissions to control access to specific resources or functionalities.
    *   **Input Validation:** Implement comprehensive input validation on all API endpoints to prevent common vulnerabilities like SQL injection and XSS.
    *   **HTTPS:** Ensure all communication is over HTTPS to encrypt data in transit.

## 6. API Rate Limiting

*   **Strategy:** Implement API rate limiting to protect against abuse, denial-of-service (DoS) attacks, and to ensure fair usage of resources.
*   **Implementation Ideas:**
    *   **FastAPI Middleware:** Use a custom FastAPI middleware or a library like `fastapi-limiter` to apply rate limits based on IP address, API key (if introduced later), or user ID.
    *   **Token Bucket Algorithm:** A common algorithm for rate limiting that allows for bursts of requests.
    *   **Redis:** Use Redis as a backend for storing rate limit counters for distributed and scalable rate limiting.

## 7. Deployment Ideas

*   **Initial Deployment (Simple):**
    *   **Docker:** Containerize the FastAPI application using Docker. This provides a consistent environment across development and production.
    *   **`uvicorn` with Gunicorn:** Run `uvicorn` behind a production-ready ASGI server like Gunicorn for process management and concurrency.
    *   **Reverse Proxy:** Use Nginx or Apache as a reverse proxy to handle SSL termination, load balancing, and serving static files.
*   **Cloud Deployment (Scalable):
    *   **Platform as a Service (PaaS):** Services like Heroku, Google App Engine, or AWS Elastic Beanstalk offer simplified deployment and scaling for web applications.
    *   **Container Orchestration:** For more complex deployments, use Kubernetes (EKS, GKE, AKS) to manage containerized applications at scale.
    *   **Serverless Functions:** For specific stateless endpoints, consider AWS Lambda, Google Cloud Functions, or Azure Functions.
*   **Database Deployment:**
    *   For production, use managed database services (e.g., AWS RDS, Google Cloud SQL, Azure Database for PostgreSQL) to handle database operations, backups, and scaling.

## 8. Unit Validation for Physics Variables

*   **Tool:** `pint` (Python library)
*   **Justification:** `pint` provides a comprehensive and flexible framework for handling physical quantities with units in Python. It allows for:
    *   Defining and parsing units (e.g., `meter`, `kg`, `N`).
    *   Performing unit-aware calculations, automatically converting units when necessary.
    *   Checking unit consistency and raising errors for incompatible units.
    *   Defining custom units and contexts.
*   **Integration:** `pint` can be integrated into the backend to validate the units of known parameters and the variable to find, ensuring physical correctness before performing calculations.

## 9. Symbolic Validation of Equations

*   **Tool:** `SymPy` (Python library)
*   **Justification:** `SymPy` is a powerful Python library for symbolic mathematics. It can be used to:
    *   Parse and represent mathematical expressions symbolically.
    *   Perform symbolic manipulations (e.g., simplification, differentiation, integration).
    *   Solve equations symbolically.
    *   Check for mathematical equivalence of expressions.
*   **Integration:** `SymPy` can be used to validate user-submitted systems of equations. This could involve:
    *   Parsing the equations to ensure they are syntactically correct.
    *   Checking for consistency (e.g., number of equations vs. number of unknowns).
    *   Potentially performing basic symbolic checks to ensure the equations are well-formed and solvable.