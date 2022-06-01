import pytest
from fastapi import status
from app import models


@pytest.fixture()
def test_vote(test_posts, session):
    new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_posts[0].owner_id)
    session.add(new_vote)
    session.commit()
    return new_vote


def test_vote_on_own_post(authorized_client, test_posts):
    data = {"post_id": test_posts[1].id, "is_voted": True}
    res = authorized_client.post("/votes/", json=data)
    assert res.status_code == status.HTTP_201_CREATED


def test_vote_other_user_post(authorized_client, test_user2, test_posts):
    other_user_post_id = next(
        post.id for post in test_posts if post.owner_id == test_user2["id"]
    )
    data = {"post_id": other_user_post_id, "is_voted": True}
    res = authorized_client.post("/votes/", json=data)
    assert res.status_code == status.HTTP_201_CREATED


def test_vote_twice(authorized_client, test_vote):
    data = {"post_id": test_vote.post_id, "is_voted": True}
    res = authorized_client.post("/votes/", json=data)
    assert res.status_code == status.HTTP_409_CONFLICT


def test_delete_vote(authorized_client, test_vote):
    data = {"post_id": test_vote.post_id, "is_voted": False}
    res = authorized_client.post("/votes/", json=data)
    assert res.status_code == status.HTTP_201_CREATED


def test_delete_not_exist_post_vote(authorized_client):
    data = {"post_id": "6969", "is_voted": False}
    res = authorized_client.post("/votes/", json=data)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_not_exist_vote(authorized_client, test_posts):
    data = {"post_id": test_posts[3].id, "is_voted": False}
    res = authorized_client.post("/votes/", json=data)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_vote(client, test_vote):
    data = {"post_id": test_vote.post_id, "is_voted": False}
    res = client.post("/votes/", json=data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
