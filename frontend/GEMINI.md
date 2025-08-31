# Project Overview: PhysAI Frontend

This directory contains the frontend application for PhysAI, a web-based platform likely focused on physics education or problem-solving. It is implemented as a single-page application (SPA) using pure JavaScript, HTML, and CSS, with client-side routing to dynamically load different views.

## Technologies Used

*   **HTML, CSS, JavaScript:** Core web technologies.
*   **KaTeX:** For rendering mathematical equations.
*   **MathQuill:** For interactive mathematical input/editing (though its full usage isn't evident from the initial files).
*   **jQuery:** A JavaScript library for DOM manipulation.
*   **Marked:** A markdown parser (listed as a dependency, but its usage is not immediately apparent in the main scripts).

## Architecture

The application follows a modular structure where different sections (e.g., course selection, problem listing, problem solving) are organized as separate "views" within the `views/` directory. Each view typically consists of:

*   `index.html`: The HTML structure for the view.
*   `script.js`: JavaScript logic specific to the view.
*   `style.css`: CSS styling specific to the view.

The main `script.js` in the root directory handles the dynamic loading of these views and manages the overall client-side routing. Course and problem data are currently hardcoded within the main `script.js`.

## Building and Running

This project does not require a separate build step. It can be served directly as static files.

To run the application:

1.  **Navigate to the `frontend` directory:**
    ```bash
    cd /home/dima/projects/physai/frontend
    ```
2.  **Serve the static files:**
    Use Python's built-in HTTP server (or any other static file server):
    ```bash
    python -m http.server 8000
    ```
    (You can use any available port, e.g., `8080`.)

3.  **Access in browser:**
    Open your web browser and navigate to `http://localhost:8000/` (adjust the port if you used a different one).

## Development Conventions

*   **Client-Side Routing:** Views are loaded dynamically using `fetch` and injected into the `main-content` div in `index.html`.
*   **View-Specific Assets:** Each view (`views/<view-name>/`) encapsulates its own HTML, JavaScript, and CSS.
*   **Global Styles/Scripts:** Global `style.css` and `script.js` in the root handle overall layout, common styles, and the view loading mechanism.
*   **No Explicit Build Process:** Changes to HTML, CSS, or JavaScript files are immediately reflected upon refreshing the browser after saving.
*   **Testing:** The `package.json` contains a placeholder test script (`"test": "echo "Error: no test specified" && exit 1"`), indicating that no specific testing framework or setup is currently configured.
