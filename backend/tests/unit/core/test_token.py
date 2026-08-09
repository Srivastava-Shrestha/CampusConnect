import pytest
from app.core.token import create_access_token, create_refresh_token, decode_token
from app.exceptions import AuthenticationError


def test_create_access_token_has_correct_claims():
    """Ensure that a created access token includes type and expiration claims"""
    token = create_access_token({"sub": "1", "role": "STUDENT"})
    payload = decode_token(token, exp_type="access")
    assert payload["type"] == "access"
    assert payload["sub"] == "1"
    assert "exp" in payload


def test_create_refresh_token_has_correct_claims():
    """Ensure that a created refresh token includes type and expiration claims"""
    token = create_refresh_token({"sub": "1", "role": "STUDENT"})
    payload = decode_token(token, exp_type="refresh")
    assert payload["type"] == "refresh"
    assert payload["sub"] == "1"


def test_decode_token_wrong_type_fails():
    """Ensure that decoding fails when a refresh token is supplied where an access token is expected"""
    token = create_refresh_token({"sub": "1", "role": "STUDENT"})
    with pytest.raises(AuthenticationError):
        decode_token(token, exp_type="access")


def test_decode_token_invalid_signature_fails():
    """Ensure that decoding fails when a token with an invalid signature is provided"""
    with pytest.raises(AuthenticationError):
        decode_token("not.a.valid.token", exp_type="access")
