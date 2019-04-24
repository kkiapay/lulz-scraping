setup: flask-env/bin/activate

flask-env/bin/activate: requirements.txt
	test -d flask-env || virtualenv flask-env
	. flask-env/bin/activate; pip install -Ur requirements.txt

run_dev:
	. flask-env/bin/activate && python run.py