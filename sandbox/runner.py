import tempfile
from pathlib import Path
from tempfile import TemporaryDirectory

from sandbox.git import clone_repository
from sandbox.executor import run_command

def run_sandbox(repo_url: str, command: list[str]):
    with TemporaryDirectory() as tmp_dir:
        repo_path = Path(tmp_dir)

        print(f"Cloning repository {repo_url} to {repo_path}")

        clone_repository(
            repo_url,
            repo_path
        )

        print("Repository cloned")
        print(f"Running command: {' '.join(command)}")

        result = run_command(
            command,
            repo_path
        )

        status_result = run_command(
            ["git", "status", "--short"],
            repo_path
        )

        run_command(
            ["git", "add", "-A"],
            repo_path
        )

        diff_result = run_command(
            ["git", "diff", "--cached", "--binary"],
            repo_path
        )

        result["git_diff"] = diff_result["stdout"]
        result["changed_files"] = status_result["stdout"]

        return result