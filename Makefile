setup: flask-env/bin/activate

flask-env/bin/activate: requirements.txt
	test -d flask-env || virtualenv flask-env
	. flask-env/bin/activate; pip install -Ur requirements.txt

run_dev:
	. flask-env/bin/activate && python run.py

run_prod:
	. flask-env/bin/activate && APPLICATION_ENV="Production" gunicorn --bind 0.0.0.0:8080 run:app

run_docker:
	gunicorn run:app --bind 0.0.0.0:8080 --access-logfile=logs/gunicorn-access.log --error-logfile logs/gunicorn-error.log