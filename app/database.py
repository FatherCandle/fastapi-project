from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 'postgresql://<username>:<password>@<ip-adress/hostname:port>/<database_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# DB connection before I used SQLalchemy
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password=f"{settings.db_password}",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("DB connected")
#         break
#     except Exception as e:
#         print("DB failed")
#         print("Error", e)
#         time.sleep(5)
