from jyl import db
from jyl.models import *

users = User.query.all()

for user in users:
    user.confirmed = True
    db.session.commit()
    print(user.firstname)
    print(user.confirmed)