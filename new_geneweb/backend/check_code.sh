poetry run pytest --maxfail=1 --disable-warnings -q --cov=app --cov-report=xml
poetry run coverage report
poetry run ruff check --fix .
poetry run black .
poetry run mypy app/