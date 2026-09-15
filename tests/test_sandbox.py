from sandbox.runner import run_sandbox

TEST_REPO = "https://github.com/octocat/Hello-World.git"

def test_sandbox_can_create_file():
    result = run_sandbox(
        TEST_REPO,
        [
            "python",
            "-c",
            "open('hello.txt', 'w').write('hello')",
        ]
    )

    assert result["exit_code"] == 0
    assert "hello.txt" in result["changed_files"]
    assert "hello.txt" in result["git_diff"]


def test_sandbox_has_no_network():
    result = run_sandbox(
        TEST_REPO,
        [
            "python",
            "-c",
            "import urllib.request; urllib.request.urlopen('https://example.com', timeout=5)",
        ]
    )

    assert result["exit_code"] != 0


def test_sandbox_can_run_python():
    result = run_sandbox(
        TEST_REPO,
        [
            "python",
            "-c",
            "print('hello from sandbox')",
        ]
    )

    assert result["exit_code"] == 0
    assert "hello from sandbox" in result["stdout"]


def test_sandbox_runs_as_non_root():
    result = run_sandbox(
        TEST_REPO,
        [
            "python",
            "-c",
            "import os; print(os.getuid())",
        ],
    )

    assert result["exit_code"] == 0
    assert result["stdout"].strip() != "0"


def test_sandbox_reports_command_failure():
    result = run_sandbox(
        TEST_REPO,
        [
            "python",
            "-c",
            "raise RuntimeError('intentional failure')",
        ],
    )

    assert result["exit_code"] != 0
    assert "intentional failure" in result["stderr"]


def test_sandbox_times_out():
    result = run_sandbox(
        TEST_REPO,
        [
            "python",
            "-c",
            "import time; time.sleep(70)",
        ],
    )

    assert result["exit_code"] == -1
    assert "timed out" in result["stderr"].lower()