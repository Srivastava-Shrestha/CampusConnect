import pytest
from app.core.token import create_access_token, create_refresh_token, decode_token
from app.exceptions import AuthenticationError


def test_create_access_token_has_correct_claims():
    """Access token should include type and expiration"""
    token = create_access_token({"sub": "1", "role": "STUDENT"})
    payload = decode_token(token, exp_type="access")
    assert payload["type"] == "access"
    assert payload["sub"] == "1"
    assert "exp" in payload


def test_create_refresh_token_has_correct_claims():
    """Refresh token should include type and expiration"""
    token = create_refresh_token({"sub": "1", "role": "STUDENT"})
    payload = decode_token(token, exp_type="refresh")
    assert payload["type"] == "refresh"
    assert payload["sub"] == "1"


def test_decode_token_wrong_type_fails():
    """Passing a refresh token where an access token is expected should fail"""
    token = create_refresh_token({"sub": "1", "role": "STUDENT"})
    with pytest.raises(AuthenticationError):
        decode_token(token, exp_type="access")


def test_decode_token_invalid_signature_fails():
    """A token with a broken signature should be rejected"""
    with pytest.raises(AuthenticationError):
        decode_token("not.a.valid.token", exp_type="access")
