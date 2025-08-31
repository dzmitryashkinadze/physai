import subprocess
import os
import tempfile

def execute_user_code(code: str, test_input: str) -> str:
    """Executes user-submitted Python code in a sandboxed environment.

    For now, this is a basic implementation. In a production environment,
    this would involve Docker containers for true isolation.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "user_code.py")
        with open(file_path, "w") as f:
            f.write(code)

        # For now, a simple subprocess call. This needs to be replaced with Docker.
        try:
            # Pass test_input to the script via stdin
            process = subprocess.run(
                ["python", file_path],
                input=test_input.encode('utf-8'),
                capture_output=True,
                text=True,
                timeout=5  # Basic timeout
            )
            if process.returncode != 0:
                return f"Runtime Error: {process.stderr}"
            return process.stdout
        except subprocess.TimeoutExpired:
            return "Runtime Error: Code execution timed out."
        except Exception as e:
            return f"Runtime Error: {str(e)}"
