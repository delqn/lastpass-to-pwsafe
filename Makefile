SHELL=bash

.PHONY: convert
convert:
	./lastpass-to-pwsafe.py ./passwords.tsv ./pwsafe.csv

.PHONY: test
test:
	PYTHONPATH=$PYTHONPATH:./ python2.7 ./tests/test_pwdb_convert.py

.PHONY: lint
lint:
	pep8 flatten_json/
	pylint --rcfile=.pylintrc flatten_json/

.PHONY: clean
clean:
	find . -name \*.pyc -delete

.PHONY: requirements
requirements:
	pip install -r requirements.txt
