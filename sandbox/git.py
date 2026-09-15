import subprocess
from pathlib import Path

def clone_repository(repo_url: str, destination: Path):
    subprocess.run(
        ["git", "clone", repo_url, str(destination)],
        check=True
    )


