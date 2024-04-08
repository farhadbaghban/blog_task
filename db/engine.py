from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker
import time

# SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@mysql:3306/blog_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Retry connecting to the database
max_retries = 5
retry_delay = 5  # seconds

for _ in range(max_retries):
    try:
        engine.connect()
        break
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        print("Retrying in {} seconds...".format(retry_delay))
        time.sleep(retry_delay)
else:
    print(
        "Failed to connect to the database after {} retries. Exiting...".format(
            max_retries
        )
    )
    exit(1)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
