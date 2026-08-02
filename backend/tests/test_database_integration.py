from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"
DOCKER_CONFIG_DIR = PROJECT_ROOT / ".docker-tmp"
DOCKER_TEST_PROJECT = "heppysitousato-dbtests"
INTEGRATION_ENV_VAR = "RUN_DOCKER_INTEGRATION_TESTS"
POSTGRES_READY_TIMEOUT_SECONDS = 90


def docker_integration_enabled() -> bool:
    return os.environ.get(INTEGRATION_ENV_VAR) == "1"


def docker_compose(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    DOCKER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    env["DOCKER_CONFIG"] = str(DOCKER_CONFIG_DIR)

    completed = subprocess.run(
        ["docker", "compose", "-p", DOCKER_TEST_PROJECT, *args],
        cwd=PROJECT_ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    if check and completed.returncode != 0:
        raise AssertionError(
            "Docker command failed:\n"
            f"command: docker compose -p {DOCKER_TEST_PROJECT} {' '.join(args)}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return completed


def docker_daemon_available() -> tuple[bool, str]:
    env = os.environ.copy()
    DOCKER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    env["DOCKER_CONFIG"] = str(DOCKER_CONFIG_DIR)

    completed = subprocess.run(
        ["docker", "info"],
        cwd=PROJECT_ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode == 0:
        return True, ""

    diagnostic = completed.stderr.strip() or completed.stdout.strip() or "unknown error"
    return False, diagnostic


def backend_container_command(*args: str) -> subprocess.CompletedProcess[str]:
    return docker_compose(
        "run",
        "--rm",
        "--no-deps",
        "-T",
        "backend",
        *args,
    )


def extract_last_output_line(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        raise AssertionError("Command completed without stdout.")
    return lines[-1]


@pytest.fixture(scope="module")
def docker_postgres_environment() -> None:
    if not docker_integration_enabled():
        pytest.skip(f"Set {INTEGRATION_ENV_VAR}=1 to run Docker integration tests.")
    if shutil.which("docker") is None:
        pytest.skip("Docker CLI non disponibile nell'ambiente corrente.")
    docker_ready, diagnostic = docker_daemon_available()
    if not docker_ready:
        pytest.skip(f"Docker daemon non disponibile per i test live: {diagnostic}")

    docker_compose("down", "--volumes", "--remove-orphans", check=False)
    docker_compose("build", "backend")
    docker_compose("up", "-d", "postgres")

    deadline = time.monotonic() + POSTGRES_READY_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        result = docker_compose(
            "exec",
            "-T",
            "postgres",
            "pg_isready",
            "-U",
            "heppysito",
            "-d",
            "heppysitousato",
            check=False,
        )
        if result.returncode == 0:
            break
        time.sleep(2)
    else:
        raise AssertionError(
            "PostgreSQL non pronto entro il timeout.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    try:
        yield
    finally:
        docker_compose("down", "--volumes", "--remove-orphans", check=False)


def test_database_session_manager_connects_to_live_postgres_via_docker(
    docker_postgres_environment: None,
) -> None:
    result = backend_container_command(
        "poetry",
        "run",
        "python",
        "tests/support/live_database_probe.py",
        "connection",
    )

    assert extract_last_output_line(result.stdout) == "connection_ok"


def test_alembic_upgrade_head_runs_live_without_creating_public_tables(
    docker_postgres_environment: None,
) -> None:
    docker_compose(
        "run",
        "--rm",
        "--no-deps",
        "-T",
        "backend",
        "poetry",
        "run",
        "alembic",
        "upgrade",
        "head",
    )

    result = backend_container_command(
        "poetry",
        "run",
        "python",
        "tests/support/live_database_probe.py",
        "public-tables",
    )
    payload = json.loads(extract_last_output_line(result.stdout))

    assert payload == {"tables": []}
