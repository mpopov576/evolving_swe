from pathlib import Path
from tempfile import TemporaryDirectory

from sandbox.git import clone_repository
from sandbox.docker_executor import run_in_docker


def run_sandbox(repo_url: str, command: list[str]):
    with TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir) / "repo"

        print(f"Cloning repository {repo_url} to {repo_path}")

        clone_repository(repo_url, repo_path)

        print("Repository cloned")
        print(f"Running command in Docker: {' '.join(command)}")

        result = run_in_docker(command, repo_path)

        status_result = run_in_docker(
            ["git", "status", "--short", "--untracked-files=all"],
            repo_path,
        )

        run_in_docker(
            ["git", "add", "-A"],
            repo_path,
        )

        diff_result = run_in_docker(
            ["git", "diff", "--cached", "--binary"],
            repo_path,
        )

        result["changed_files"] = status_result["stdout"]
        result["git_diff"] = diff_result["stdout"]

        return result
