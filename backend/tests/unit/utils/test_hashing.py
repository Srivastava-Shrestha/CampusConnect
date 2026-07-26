from app.utils.hashing import hash_password, verify_password


def test_hash_password_is_not_plain_text():
    """Ensure that the hashed password does not match the original plain text"""
    hashed = hash_password("MyPassword123")
    assert hashed != "MyPassword123"
    assert isinstance(hashed, str)


def test_verify_password_success():
    """Ensure that a correct password successfully verifies against its hash"""
    hashed = hash_password("MyPassword123")
    assert verify_password("MyPassword123", hashed) is True


def test_verify_password_failure():
    """Ensure that an incorrect password fails to verify against the hash"""
    hashed = hash_password("MyPassword123")
    assert verify_password("WrongPassword", hashed) is False
