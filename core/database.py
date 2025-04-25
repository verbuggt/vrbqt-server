from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from util import load_secret_str

# OBSOLETE # SQLALCHEMY_DATABASE_URL = "sqlite:///./vrbqt.db"
secret = load_secret_str("core.db_pass")
# SQLALCHEMY_DATABASE_URL = f"postgresql://vrbqt:{secret}@localhost/vrbqtdb"
SQLALCHEMY_DATABASE_URL = "sqlite:///./vrbqt.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> sessionmaker:
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
