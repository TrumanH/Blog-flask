class Config(object):
    SECRET_KEY = 'f3cf8ce6a025a73e56dd6761eb7d1575'

class ProdConfig():
    pass

class DevConfig(object):
    DEBUG = True
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

    
