import pytest
from digeiz_api.api import app, get_db
from digeiz_api.db import crud, schemas
from fastapi.testclient import TestClient


def test_api_get_accounts(session, created_accounts, client):
    response = client.get(f"/accounts")
    assert response.status_code == 200
    assert len(response.json()) == 10  # limit to 10


def test_api_create_accounts(session, client):
    response = client.post("/accounts/",
                           json={
                               "name": "test",
                               "email": "admin@test.com",
                               "password": "not_a_pass"
                           })
    assert response.status_code == 200
    response_duplicate = client.post("/accounts/",
                                     json={
                                         "name": "test",
                                         "email": "admin@test.com",
                                         "password": "not_a_pass"
                                     })
    assert response_duplicate.status_code == 400


@pytest.mark.parametrize("account_id,status_code", [(1, 200), (34333, 404)])
def test_api_get_account(session, created_accounts, client, account_id,
                         status_code):
    response = client.get(f"/accounts/{account_id}")
    assert response.status_code == status_code
    if status_code == 200:
        for k in ["email", "name", "id", "hashed_password", "is_active"]:
            assert k in response.json().keys() and k != None


@pytest.mark.parametrize("account_id,status_code", [(4, 200), (34333, 404)])
def test_api_delete_account(session, created_accounts, client, account_id,
                            status_code):
    response = client.delete(f"/accounts/{account_id}")
    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()['id'] == account_id


@pytest.mark.parametrize("account_id,status_code", [(4, 200), (34333, 404)])
def test_api_modify_account_name(session, created_accounts, client, account_id,
                                 status_code):
    response = client.patch(f"/accounts/{account_id}",
                            json={"name": "new_name"})
    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()['id'] == account_id


def test_api_create_mall(session, created_accounts, client):
    response = client.post("/malls/", json={"name": "test", "account": 1})
    assert response.status_code == 200
    response_duplicate = client.post("/malls/",
                                     json={
                                         "name": "test",
                                         "account": 2
                                     })
    assert response_duplicate.status_code == 400
    # response_duplicate = client.post("/malls/",
    #                                  json={
    #                                      "name": "test",
    #                                      "email": "admin@test.com",
    #                                      "password": "not_a_pass"
    #                                  })
    # assert response_duplicate.status_code == 400


@pytest.mark.parametrize("unit_id,status_code", [(1, 200), (34333, 404)])
def test_api_get_unit(session, created_malls, client, unit_id, status_code):
    response = client.get(f"/malls/{unit_id}")
    assert response.status_code == status_code
    if status_code == 200:
        for k in ["name", "id", "is_active"]:
            assert k in response.json().keys() and k != None


def test_api_get_units(session, created_units, client):
    response = client.get(f"/units")
    assert response.status_code == 200
    assert len(response.json()) == len(created_units)


@pytest.mark.parametrize("unit_id,status_code", [(2, 200), (34333, 404)])
def test_api_delete_unit(session, created_units, client, unit_id, status_code):
    response = client.delete(f"/units/{unit_id}")
    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()['id'] == unit_id


# @pytest.mark.parametrize("mall_id,status_code", [(1, 200), (34333, 404)])
# def test_api_modify_mall_name(session, created_units, client, mall_id,
#                               status_code):
#     response = client.patch(f"/malls/{mall_id}", json={"name": "new_name"})
#     assert response.status_code == status_code
#     if status_code == 200:
#         assert response.json()['id'] == mall_id


def test_api_create_unit(session, created_accounts, client):
    response = client.post("/units/", json={"name": "test"})
    assert response.status_code == 200
    response_duplicate = client.post("/units/", json={"name": "test"})
    assert response_duplicate.status_code == 400