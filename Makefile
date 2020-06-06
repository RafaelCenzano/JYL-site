init:
	pip3 install -r requirements.txt

clean:
	pystarter clean

update:
	pip install --upgrade alembic apscheduler bcrypt blinker cffi click dnspython email-validator flask flask-bcrypt flask-login flask-mail flask-migrate flask-script flask-sqlalchemy flask-wtf gunicorn idna itsdangerous jinja2 mako markupsafe pip psycopg2-binary pycparser pystarter python-dateutil python-editor pytz setuptools six sqlalchemy tzlocal werkzeug wheel wtforms
	pip freeze > requirements.txt

run: clean
	gunicorn run:app --reload

test: clean
	python runtest.py

stresstest: clean
	gunicorn run:app -w 6 --preload --max-requests-jitter 300