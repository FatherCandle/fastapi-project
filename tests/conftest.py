from fastapi.testclient import TestClient
import pytest
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app import models
from app.main import app
from app.config import settings
from app.oauth2 import create_access_token
from app.database import get_db, Base


# 'postgresql://<username>:<password>@<ip-adress/hostname:port>/<database_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session() -> Session:
    # The drop and create can be made with alembic
    # using: command.upgrade(<version_id>) and command.downgrade(<version_id>)

    # Drop all the tables to clear the db before the test
    Base.metadata.drop_all(bind=engine)
    # Create all tables before the test
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == status.HTTP_201_CREATED

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "test321@gmail.com", "password": "password321"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == status.HTTP_201_CREATED

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session: Session):
    posts_data = [
        {"title": "1 title", "content": "1 content", "owner_id": test_user["id"]},
        {"title": "2 title", "content": "2 content", "owner_id": test_user["id"]},
        {"title": "3 title", "content": "3 content", "owner_id": test_user["id"]},
        {"title": "4 title", "content": "4 content", "owner_id": test_user2["id"]},
    ]

    posts_models = [models.Post(**post) for post in posts_data]
    session.add_all(posts_models)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
