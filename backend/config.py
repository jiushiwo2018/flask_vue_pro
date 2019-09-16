import os
basedir = os.path.abspath(os.path.dirname(__file__))
###得到程序根目录的位置（去掉最底层文件名）
###基类Config包含通用配置，子类分别定义专用的配置。
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    ###某些配置如敏感信息可以从环境变量中导入，系统也可提供一个默认值，以防环境中没有定义。
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ###配置对象中还有一个很有用的选项，即SQLALCHEMY_COMMIT_ON_TEARDOWN键，将其设为True时，每次请求结束后都会自动提交数据库中的变动。
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    ###flask_mail的主题前缀设置
    FLASKY_MAIL_SENDER = 'gary_cxd@126.com'
    ###flask_mail的发送者邮件设置
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    ###从环境中设置管理员的邮件地址，用于接收通知新用户注册邮件，这里面的发送者sender，接受者ADMIN都是自己。


    ###一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。
    ###而使用'@staticmethod'或'@classmethod'，就可以不需要实例化，直接类名.方法名()来调用。
    ###详细请见另一个博客。

    @staticmethod
    def init_app(app):
        pass
    ###配置类可以定义init_app()方法类，其参数是程序实例。
    ###在这个方法中。可以执行对当前环境的配置初始化。
    ###基类Config中的init_app()方法为空。
class DevelopmentConfig(Config):
    DEBUG = True
    ###调试模式开启，不懂什么意思。
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://chenxudx_so:i8r1v9t5i2xB2Yo@maria3321-us-fm-in.icloud.intel.com:3306/test_flasy_schema"

    AUTH_LDAP_SERVER_URI = "ldap://corpad.glb.intel.com"
    LDAP_SERVER_PORT = 3268
    ADMIN_DN = "cn=TSIE LDAP,ou=DC,ou=MCG TSIE,ou=Resources,dc=ccr,dc=corp,dc=intel,dc=com"
    ADMIN_PASSWORD = "intel123!"
    SEARCH_BASE = "ou=Workers,dc=ccr,dc=corp,dc=intel,dc=com"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://chenxudx_so:i8r1v9t5i2xB2Yo@maria3321-us-fm-in.icloud.intel.com:3306/test_flasy_schema"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://chenxudx_so:i8r1v9t5i2xB2Yo@maria3321-us-fm-in.icloud.intel.com:3306/test_flasy_schema"

config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
###在这个配置脚本末尾，config字典中注册了不同的配置环境，而且还注册了一个默认配置。