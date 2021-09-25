import pytest
from http import HTTPStatus


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        json={
            "username": "michael",
            "email": "michael@testdriven.io",
        },
    )
    data = resp.json
    assert resp.status_code == HTTPStatus.CREATED
    assert "michael@testdriven.io was added!" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/users", json={})
    data = resp.json
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/users", json={"email": "john@testdriven.io"})
    data = resp.json
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        json={"username": "michael", "email": "michael@testdriven.io"},
    )
    resp = client.post(
        "/users", json={"username": "michael", "email": "michael@testdriven.io"}
    )
    data = resp.json
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert "Sorry. That email already exists." in data["message"]


def test_single_user(test_app, test_database, add_user):
    user = add_user("jeffrey", "jeffrey@testdriven.io")
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = resp.json
    assert resp.status_code == 200
    assert "jeffrey" in data["username"]
    assert "jeffrey@testdriven.io" in data["email"]


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = resp.json
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_all_users(test_app, test_database, add_user):
    add_user("michael", "michael@mherman.org")
    add_user("fletcher", "fletcher@notreal.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = resp.json
    assert resp.status_code == 200
    assert len(data) == 2
    assert "michael" in data[0]["username"]
    assert "michael@mherman.org" in data[0]["email"]
    assert "fletcher" in data[1]["username"]
    assert "fletcher@notreal.com" in data[1]["email"]


def test_remove_user(test_app, test_database, add_user):
    user = add_user("user-to-be-removed", "remove-me@testdriven.io")
    client = test_app.test_client()
    resp_one = client.get("/users")
    data = resp_one.json
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"/users/{user.id}")
    data = resp_two.json
    assert resp_two.status_code == 200
    assert "remove-me@testdriven.io was removed!" in data["message"]

    resp_three = client.get("/users")
    data = resp_three.json
    assert resp_three.status_code == 200
    assert len(data) == 0


def test_remove_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/users/999")
    data = resp.json
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_update_user(test_app, test_database, add_user):
    user = add_user("user-to-be-updated", "update-me@testdriven.io")
    client = test_app.test_client()
    resp_one = client.put(
        f"/users/{user.id}", json={"username": "me", "email": "me@testdriven.io"}
    )
    data = resp_one.json
    assert resp_one.status_code == 200
    assert f"{user.id} was updated!" in data["message"]

    resp_two = client.get(f"/users/{user.id}")
    data = resp_two.json
    assert resp_two.status_code == 200
    assert "me" in data["username"]
    assert "me@testdriven.io" in data["email"]


# fmt: off
@pytest.mark.parametrize("user_id, payload, status_code, message", [
    [1, {}, 400, "Input payload validation failed"],
    [1, {"email": "me@testdriven.io"}, 400, "Input payload validation failed"],
    [999, {"username": "me", "email": "me@testdriven.io"}, 404, "User 999 does not exist"],
])
# fmt: on
def test_update_user_invalid(
    test_app, test_database, user_id, payload, status_code, message
):
    client = test_app.test_client()
    resp = client.put(f"/users/{user_id}", json=payload)
    data = resp.json
    assert resp.status_code == status_code
    assert message in data["message"]


def test_update_user_duplicate_email(test_app, test_database, add_user):
    add_user("hajek", "rob@hajek.org")
    user = add_user("rob", "rob@notreal.com")

    client = test_app.test_client()
    resp = client.put(
        f"/users/{user.id}", json={"username": "rob", "email": "rob@notreal.com"}
    )
    data = resp.json
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]
