import pytest
from datetime import timedelta, datetime
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, status
from config.JWTUtility import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    decode_access_token,
    get_current_user,
    get_current_admin_user,
)
from schemas.UserSchema import UserSchema

@pytest.fixture(scope="module")
def mock_user_schema():
    return UserSchema(username="testuser", role="USER", password="")

@pytest.fixture(scope="module")
def valid_token():
    return create_access_token({"sub": "testuser", "role": "USER"})

@pytest.fixture(scope="module")
def invalid_token():
    return "invalid.token"

def test_create_access_token():
    token = create_access_token({"sub": "testuser", "role": "USER"})
    assert isinstance(token, str)

def test_decode_access_token(valid_token):
    payload = decode_access_token(valid_token)
    assert payload["sub"] == "testuser"
    assert payload["role"] == "USER"

def test_get_current_user_invalid_token(invalid_token):
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(invalid_token)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_admin_user_invalid_user_role(mock_user_schema):
    mock_user_schema.role = "USER"
    with pytest.raises(HTTPException) as excinfo:
        get_current_admin_user(mock_user_schema)
    assert excinfo.value.status_code == status.HTTP_403_FORBIDDEN
