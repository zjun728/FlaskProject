from flask_sqlalchemy import SQLAlchemy
from apps import app

db = SQLAlchemy(app)


class UserProfile(db.Model):  # 创建的数据库表 是类名的小写形式 即表名为；user
    __tablename__ = "userprofile"   # 若果我们不指定数据库表名则创建的数据库表名是类名的小写形式 即表名为；user 若类名为：UserProfile 则表名为：user_profile
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r, Email %r>' % (self.username, self.email)


if __name__ == "__main__":
    db.create_all()
    admin = UserProfile(username='admin', email='admin@example.com')
    guest = UserProfile(username='guest', email='guest@example.com')

    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    all = UserProfile.query.all()   # 查询不需要 commit
    print(all)
    admin_xx = UserProfile.query.filter_by(username='admin').first()
    print(admin_xx)
