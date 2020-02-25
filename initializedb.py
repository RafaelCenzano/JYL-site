from jyl import db, app, bcrypt
from jyl.models import User
from hashlib import sha256

db.create_all()

pass1 = bcrypt.generate_password_hash(
            sha256(
                ('pass' +
                 'raf@demo.com' +
                 app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()).decode('utf-8')
pass2 = bcrypt.generate_password_hash(
            sha256(
                ('pass' +
                 'rafa@demo.com' +
                 app.config['SECURITY_PASSWORD_SALT']).encode('utf-8')).hexdigest()).decode('utf-8')
user_1 = User(firstname='rafael', lastname='cenzano', email='raf@demo.com', password=pass1, confirmed=True, hours=0.0, nickname='raf', nicknameapprove=False)
db.session.add(user_1)
user_2 = User(firstname='rafael', lastname='cenzano', email='rafa@demo.com', password=pass2, confirmed=True, hours=0.0, nickname='raf', nicknameapprove=True)
db.session.add(user_2)

# commit the chagnes to the db
db.session.commit()

