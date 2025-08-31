# Frontend Application

This directory contains the pure JavaScript, HTML, and CSS frontend for the PhysAI application.

## Setup and Running

1.  **Serve the Frontend:**
    Navigate to this `frontend` directory in your terminal:
    ```bash
    cd frontend
    ```
    Then, serve the static files using Python's built-in HTTP server (or any other static file server):
    ```bash
    python -m http.server 8000 # Or any other port, e.g., 8080
    ```
    You should see output indicating the server is running, typically at `http://0.0.0.0:8000`.

2.  **Access the Frontend in your Browser:**
    Open your web browser and navigate to the application's root:
    ```
    http://localhost:8000/
    ```
    (Adjust the port if you used a different one in the previous step.)

    The application uses client-side routing. You can navigate between views using the buttons in the header or by directly accessing the following paths:
    -   `/` (Home page)
    -   `/about` (About page)
    -   `/problem-editor` (Problem Creation Form)
