# Contributing

Thank you for considering a contribution.

## Before changing code

1. Open an issue describing the bug or proposed improvement.
2. Keep changes focused and document any behavior or command changes.
3. Never commit API keys, .env files, private retail footage, or private datasets.

## Local setup

```bash
python -m venv .venv
pip install -e .
pip install -r requirements-dev.txt
```

## Checks

Run the unit tests before opening a pull request:

```bash
pytest
```

The GitHub Actions workflow runs the tests for pushes to main and pull requests targeting main.

## Pull requests

Include:
- A concise description of the change.
- Steps to reproduce or verify it.
- Test results.
- Updated documentation when commands, configuration, or behavior changes.

Do not claim model-performance improvements without a documented evaluation dataset, split, and reproducible metrics.
