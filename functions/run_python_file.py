import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            [sys.executable, abs_file_path, *args],
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True,
        )

        parts = []
        if result.stdout.strip():
            parts.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr.strip():
            parts.append(f"STDERR:\n{result.stderr.strip()}")
        if result.returncode != 0:
            parts.append(f"Process exited with code {result.returncode}")
        if not parts:
            return "No output produced."
        return "\n\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
