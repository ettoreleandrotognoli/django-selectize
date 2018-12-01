PYTHON?=venv/bin/python
COVERAGE?=venv/bin/coverage

build:
	npm run build
	${PYTHON} setup.py sdist

coverage:
	PYTHONPATH=src/python ${COVERAGE} run -m unittest discover test/python/
	PYTHONPATH=src/python ${COVERAGE} run examples/python/selectize-demo/manage.py test examples/python/selectize-demo/
	coverage report --include=src/python/*,examples/python/*
	coverage html --include=src/python/*,examples/python/*