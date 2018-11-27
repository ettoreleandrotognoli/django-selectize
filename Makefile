PYTHON=venv/bin/python

build:
	npm run build
	${PYTHON} setup.py sdist