import pytest
from fastapi import status
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    #   Can be used for testing the posts we got from the request
    res_posts = [schemas.PostOut(**post) for post in res.json()]

    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == len(test_posts)


def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    res_post = schemas.PostOut(**res.json())

    assert res.status_code == status.HTTP_200_OK
    assert res_post.Post.id == test_posts[0].id


def test_get_not_exist_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/6969")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("title1", "content1", False),
        ("title2", "content2", True),
        ("title3", "content3", False),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published},
    )

    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


@pytest.mark.parametrize(
    "title, content",
    [
        ("title1", "content1"),
        ("title2", "content2"),
        ("title3", "content3"),
    ],
)
def test_create_post_default_published_true(
    authorized_client, test_user, test_posts, title, content
):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content},
    )

    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client):
    res = client.post(
        "/posts/",
        json={"title": "title1", "content": "content1"},
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_exist_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/6969")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_user_post(authorized_client, test_user2, test_posts):

    other_user_post_id = next(
        post.id for post in test_posts if post.owner_id == test_user2["id"]
    )
    res = authorized_client.delete(f"/posts/{other_user_post_id}")
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_unauthorized_user_update_post(client, test_user, test_posts):

    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }

    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_not_exist_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": "6969",
    }
    res = authorized_client.put(f"/posts/{data['id']}", json=data)
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_other_user_post(authorized_client, test_user2, test_posts):
    other_user_post_id = next(
        post.id for post in test_posts if post.owner_id == test_user2["id"]
    )
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": other_user_post_id,
    }
    res = authorized_client.put(f"/posts/{other_user_post_id}", json=data)
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    udpated_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert udpated_post.title == data["title"]
    assert udpated_post.content == data["content"]
