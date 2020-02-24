from jyl import db

user_1 = User(firstname='rafael', lastname='cenzano', email='r@demo.com', password='pass', confirmed=True, hours=0.0, nickname='raf', nicknameapprove=False)
db.session.add(user_1)
user_2 = User(firstname='rafael', lastname='cenzano', email='ra@demo.com', password='pass', confirmed=True, hours=0.0, nickname='raf', nicknameapprove=True)
db.session.add(user_2)