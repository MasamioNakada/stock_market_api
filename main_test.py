from fastapi.testclient import TestClient

import json

from main import app

from routers.utils import db

client = TestClient(app)


# Fake Credentials for testing
fake_user_full_name = "Test User"
fake_user_email = "testing@example.com"
fake_user_password = "testing123"
fake_token = "b4d6dd3a7f3e6294"


# Test the root path
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Reply": "Stock Market API Service"}



# Test the /users/create_user endpoint
def test_good_create_user():
    user_data : dict[str,str]= {
        "full_name": fake_user_full_name,
        "email": fake_user_email,
        "password": fake_user_password
    }
    response = client.post("/users/create_user", json=user_data)

    assert response.status_code == 201
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"
    assert isinstance(response.json()["expires_in"],str) 

def test_bad_create_user():
    user_data : dict[str,str] = {
        "full_name": fake_user_full_name,
        "email": fake_user_email,
        "password": fake_user_password
    }
    response = client.post("/users/create_user", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"


# Test the /users/get_access_token endpoint
def test_good_get_access_token():
    response = client.get("/users/get_access_token", auth=(fake_user_email, fake_user_password))
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"
    assert isinstance(response.json()["expires_in"],str)

def test_bad_get_access_token():
    response = client.get("/users/get_access_token", auth=(fake_user_email, "bad_password"))
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

# Test the /api/get_stock endpoint
def test_good_get_stock():
    symbol = "AAPL"
    response = client.get("/users/get_access_token", auth=(fake_user_email, fake_user_password))
    access_token :str =  response.json()["access_token"] 

    response = client.get(f"/api/stock/{symbol}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["symbol"] == symbol
    assert isinstance(response.json()["open"],str)
    assert isinstance(response.json()["high"],str)
    assert isinstance(response.json()["low"],str)
    assert isinstance(response.json()["variation"],str)

def test_bad_get_stock():
    symbol = "BAD_SYMBOL"
    response = client.get("/users/get_access_token", auth=(fake_user_email, fake_user_password))
    access_token :str =  response.json()["access_token"] 

    response = client.get(f"/api/stock/{symbol}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY_ADJUSTED."

def test_bad_get_stock_bad_token():
    symbol = "AAPL"
    response = client.get(f"/api/stock/{symbol}", headers={"Authorization": f"Bearer {fake_token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
    db.delete_one("users", {"email": fake_user_email})



