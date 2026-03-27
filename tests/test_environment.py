import os

def test_env_file_exists():
    """Verify that the .env.example file exists at the root."""
    assert os.path.exists(".env.example"), ".env.example should exist in the root directory"

def test_docker_compose_exists():
    """Verify that the docker-compose.yml file exists."""
    assert os.path.exists("docker-compose.yml"), "docker-compose.yml should exist"

def test_ai_app_initialized():
    """Verify the AI layer has been initialized."""
    assert os.path.exists("ai/app/main.py"), "FastAPI main.py should exist"
    assert os.path.exists("ai/pyproject.toml"), "ai/pyproject.toml should exist"
