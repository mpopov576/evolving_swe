import subprocess
from pathlib import Path


DOCKER_IMAGE = "evolving-swe-sandbox:1.0"


def run_in_docker(command: list[str], working_directory: Path):
    try:
        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--memory", "512m",
                "--cpus", "1",
                "--pids-limit", "128",
                "--network", "none",
                "--cap-drop", "ALL",
                "--security-opt", "no-new-privileges:true",
                "--read-only",
                "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
                "-v",
                f"{working_directory}:/workspace",
                "-w",
                "/workspace",
                "-e",
                "GIT_CONFIG_COUNT=1",
                "-e",
                "GIT_CONFIG_KEY_0=safe.directory",
                "-e",
                "GIT_CONFIG_VALUE_0=/workspace",

                DOCKER_IMAGE,

                *command,
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": "Command timed out after 60 seconds.",
        }

    except FileNotFoundError:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": "Docker executable was not found.",
        }

    except OSError as error:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Failed to start Docker: {error}",
        }
