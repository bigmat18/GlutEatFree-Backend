import pytest
from utils.generate_random_string import generate_random_string


@pytest.fixture()
def tokens(client):
    response = client.post('/login', json={"email": "admin@admin.com", 
                                           "password":"admin123456"})
    return response.json()

@pytest.fixture()
def access_authorization(tokens):
    return {'Authorization': f"Bearer {tokens['access_token']}"}
    
@pytest.fixture()
def refresh_authorization(tokens):
    return {'Authorization': f"Bearer {tokens['refresh_token']}"}


@pytest.mark.parametrize("email, password, status_code",[
    ("admin@admin.com", "admin123456", 200),
    ("test@test.com", "admin123456", 400),
    ("admin@admin.com", "error", 400)
])
def test_login(client, email, password, status_code):
    response = client.post('/login', json={"email": email, "password": password})
    assert response.status_code == status_code
    
    
def test_logout(client, access_authorization):
    response = client.get('/logout', headers=access_authorization)
    assert response.status_code == 200
    

@pytest.mark.parametrize("email, password, first_name, last_name, image, status_code", [
    ("test", "test123456", "test", "test", None, 422), # Error email format
    ("admin@admin.com", "test123456", "test", "test", None, 400), # Error email altredy exists
    
    (f"{generate_random_string(5)}@test.com", "test123456", "test", "test", None, 201), # correct without image
        
    (f"test@test.com", "test123456", f"{generate_random_string(65)}", "test", None, 400), # first_name too long
    (f"test@test.com", "test123456", "test", f"{generate_random_string(65)}",None, 400) # last_name too long
])
def test_registration(client, email, password, first_name, last_name, image, status_code):
    data = {"email": email, "password": password, "first_name": first_name, "last_name": last_name}
    response = client.post('/registration', data=data)
    assert response.status_code == status_code

    
def test_refresh_token(client, refresh_authorization):
    response = client.get('/token/refresh', headers=refresh_authorization)
    assert response.status_code == 200