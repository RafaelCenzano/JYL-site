init:
	pip3 install -r requirements.txt

clean:
	pystarter clean

update:
	pip install --upgrade alembic bcrypt blinker cffi click flask flask-bcrypt flask-login flask-mail flask-migrate flask-script flask-sqlalchemy flask-wtf gunicorn itsdangerous jinja2 mako markupsafe pip pyscopg2-binary pystarter python-dateutil python-editor setuptools siz sqlalchemy wekzeug wheel wtforms

run: clean
	gunicorn run:app