from app.utils.hashing import hash_password, verify_password


def test_hash_password_is_not_plain_text():
    """Hashed password should not match the original plain text"""
    hashed = hash_password("MyPassword123")
    assert hashed != "MyPassword123"
    assert isinstance(hashed, str)


def test_verify_password_success():
    """Correct password should verify against its hash"""
    hashed = hash_password("MyPassword123")
    assert verify_password("MyPassword123", hashed) is True


def test_verify_password_failure():
    """Wrong password should not verify against the hash"""
    hashed = hash_password("MyPassword123")
    assert verify_password("WrongPassword", hashed) is False
