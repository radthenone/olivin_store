## Steps:

### Install

- pip install uv
- uv venv
- uv pip compile pyproject.toml -o requirements.txt
- uv pip sync requirements.txt
- uv pip install -r requirements.txt
