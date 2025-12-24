from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
#SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:sukanta@localhost/practice"
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()
#dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# import pymysql.connections
# try:
#     global cursor
#     connection = pymysql.connect(
#         host='localhost', user='root', password='sukanta', database='practice', cursorclass=pymysql.cursors.DictCursor)
#     cursor = connection.cursor()
# except Exception as e:
#     print(e)

