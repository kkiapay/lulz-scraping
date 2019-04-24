setup: flask-env/bin/activate

flask-env/bin/activate: requirements.txt
	test -d flask-env || virtualenv flask-env
	. flask-env/bin/activate; pip install -Ur requirements.txt

run_dev:
	source flask-env/bin/activate && python run.py

run_prod:
	. venv/bin/activate && APPLICATION_ENV="Production" gunicorn -k gevent --bind 0.0.0.0:8080 run:app