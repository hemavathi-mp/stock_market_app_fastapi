

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextvars import ContextVar
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
HOST = os.environ.get("DB_DEFAULT_HOSTNAME")
PORT = os.environ.get("DB_DEFAULT_PORT")
USERNAME = os.environ.get("DB_DEFAULT_USERNAME")
PASS = os.environ.get("DB_DEFAULT_PASSWORD")
DBNAME = os.environ.get("DB_DEFAULT_DATABASE_NAME")

# print(HOST)  # This will print "value for development" when running on local

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:active36@127.0.0.1:3306/trackado_mrc" #localhost
URL = "mysql+pymysql://"+USERNAME+":"+PASS+"@"+HOST+":"+PORT+"/"+DBNAME  #beta old server
SQLALCHEMY_DATABASE_URL = URL
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://trackado:Nawb5OcPykpev@149.102.129.245:3306/trackado_mrc" # new server
# engine = create_engine("mysql+pymysql://root:active36@127.0.0.1:3306/trackado_mrc")

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL, pool_size=50, max_overflow=0, pool_pre_ping=True, pool_recycle=300
) 
#connect_args={"check_same_thread": False}
#...is needed only for SQLite. It's not needed for other databases.

meta = MetaData()
conn = engine.connect()
DB_BASE = declarative_base()
SessionLocal = sessionmaker(bind= engine, autocommit=False, autoflush=False)

# print (conn)

async def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db_session: ContextVar[Session] = ContextVar('db_session')
