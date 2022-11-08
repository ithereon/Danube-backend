.PHONY: all fixtures static locale

all: test clean lint
exit_status = 0

test:
	mkdir -p reports; touch reports/coverage.xml; chmod -R 777 reports
	pytest ${APP}
	chmod -R 777 reports

lint:
	black danube --check
	flake8
	mypy danube
	isort -c --recursive
	bandit -s B101 -r danube
	pylint danube

static:
	python3 manage.py collectstatic --noinput

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

locale:
	python3 manage.py makemessages --all
	python3 manage.py compilemessages

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	isort -y --recursive
	black .