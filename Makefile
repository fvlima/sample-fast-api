test:
	poetry run pytest -v


install:
	poetry install

run:
	poetry run uvicorn sample_fast_api.main:app --reload

