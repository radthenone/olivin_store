## Steps:

### Install

```bash
# install uv
pip install uv
```

```bash
# create virtual environment
uv venv
```

```bash
# install pack-name
uv pip install <pack-name>
```

```bash
# add installations to requirements
uv pip freeze | uv pip compile - -o requirements.txt
```

```bash
# sync requirements is good package
uv pip sync requirements.txt
```

```bash
# install all from requirements
uv pip install -r requirements.txt
```
