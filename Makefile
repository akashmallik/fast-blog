install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements_dev.txt

run:
	uvicorn blog.main:app --reload
