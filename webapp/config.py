class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'f3cf8ce6a025a73e56dd6761eb7d1575'
    #Recaptcha在google上注册后才能使用
    #RECAPTCHA_PUBLIC_KEY = '6LdKkQQTAAAAAEHOGFj7NLg5tGicaoOus7G 9Q5Uw'
    #RECAPTCHA_PRIVATE_KEY = '6LdKkQQTAAAAAMYroksPTJ7pWhobYb88fTAcxcYn'

class ProdConfig():
    pass

class DevConfig(object):
    DEBUG = True
    SECRET_KEY = 'f3cf8ce6a025a73e56dd6761eb7d1575'  #生成表单会用到CSRF
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    #SQLALCHEMY_ECHO = True  #打印生成的查询语句
'''
#SQLite
sqlite:///database.db
#MySQL
mysql+pymysql://user:password@ip:port/db_name
#Postgres
postgresql+psycopg2://user:password@ip:port/db_name
#Oracle
oracle+cx_oracle://user:password@ip:port/db_name
'''

    
