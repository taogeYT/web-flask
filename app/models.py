from . import db
import time
import uuid

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class Dsn(db.Model):
    __tablename__ = "etl_db_dsn"
    id = db.Column(db.String(50), nullable=False, primary_key=True, default=next_id)
    name = db.Column(db.String(50), nullable=False, unique=True)
    driver = db.Column(db.String(20))
    dsn = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        json_user = self.__dict__.copy()
        json_user.pop('_sa_instance_state')
        return json_user

    @classmethod
    def find_by_cookie(cls, cookie):
        if not cookie:
            return None
        else:
            return cookie.split('-')

    def signin(self, response, max_age=86400):
        expires = str(int(time.time() + max_age))
        s = '%s-%s-%s-%s' % (self.id, self.password, expires, current_app.config['COOKIE_KEY'])
        L = [self.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
        response.set_cookie(current_app.config['COOKIE_NAME'], '-'.join(L), max_age, httponly=True)
        return response


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(50), nullable=False, primary_key=True, default=next_id)
    email = db.Column(db.String(50), nullable=False, unique=True, index=True)
    password = db.Column(db.String(50), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    image = db.Column(db.String(500), nullable=False, default='/static/img/user.png')
    created_at = db.Column(db.Float, nullable=False, default=time.time)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     db.session.add(self)
    #     db.session.commit()
# db.create_all()
