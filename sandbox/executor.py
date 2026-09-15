import subprocess
from pathlib import Path

def run_command(command: list[str], working_dir: Path):
    result = subprocess.run(
        command,
        cwd=working_dir,
        capture_output=True,
        text=True,
        timeout=60
    )

    return {
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

