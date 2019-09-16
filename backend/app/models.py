from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from ldap3 import Server, Connection, ALL, SUBTREE, ServerPool, ALL_ATTRIBUTES


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BaseException:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


class TmpUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

    def __init__(self, username):
        self.username = username

    @staticmethod
    def check_user_dn(username):
        server = Server(current_app.config['AUTH_LDAP_SERVER_URI'], port=current_app.config['LDAP_SERVER_PORT'], get_info=ALL, use_ssl=True, connect_timeout=60)
        conn = Connection(
            server,
            user=current_app.config['ADMIN_DN'],
            password=current_app.config['ADMIN_PASSWORD'],
            auto_bind=True,
            # authentication=NTLM,
            check_names=True,
            lazy=False,
            raise_exceptions=False)

        conn.open()
        conn.bind()

        res = conn.search(
            search_base=current_app.config['SEARCH_BASE'],
            search_filter='(sAMAccountName={})'.format(username),
            # search_filter='(objectclass=user)',
            # search_filter="(objectclass=organizationalUnit)",
            search_scope=SUBTREE,
            # attributes=ALL_ATTRIBUTES,
            # paged_size=2
        )

        if res:
            return conn.response[0]["dn"]
        else:
            return False

    @staticmethod
    def try_ldap_login(userdn, password):
        # userdn = username + current_app.config['LDAP_USERDN_POSTFIX']
        # userdn = "CN=Chen\\, XudongX,OU=Workers,DC=ccr,DC=corp,DC=intel,DC=com"
        # server = ServerPool(current_app.config['LDAP_SERVER'])
        server = Server(
            current_app.config['AUTH_LDAP_SERVER_URI'],
            port=current_app.config['LDAP_SERVER_PORT'],
            get_info=ALL,
            use_ssl=True,
            connect_timeout=60)
        conn = Connection(
            server,
            user=userdn,
            password=password,
            check_names=True,
            lazy=False,
            raise_exceptions=False)
        # app.logger.debug(conn)
        return conn.bind()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


# 加载用户的回调函数接收以Unicode字符串形式表示的用户标示符
# 如果能找到用户，这个函数必须返回用户对象，否则返回None。
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
