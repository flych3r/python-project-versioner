help:
	@echo "available commands"
	@echo " - venv              : creates the development environment"
	@echo " - clean             : clean temporary folders and files"
	@echo " - lint              : checks code style and type checks"
	@echo " - test              : runs all unit and integration tests"
	@echo " - coverage          : runs coverage report"
	@echo " - run-dev           : runs api in development mode"

venv:
	pipenv sync

clean:
	rm -rf `find . -type d -name .pytest_cache`
	rm -rf `find . -type d -name .mypy_cache`
	rm -rf `find . -type d -name __pycache__`
	rm -rf `find . -type d -name .ipynb_checkpoints`
	rm -f .coverage

lint: venv clean
	pipenv run flake8
	pipenv run mypy

test: venv clean
	pipenv run pytest

coverage: venv clean
	pipenv run coverage run -m pytest
	pipenv run coverage report

run-dev: venv
	pipenv run alembic upgrade head
	LOG_LEVEL=DEBUG pipenv run uvicorn app.main:app --reload
