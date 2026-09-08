"""
security.py — Password hashing and JWT creation/verification.

Why: Centralising all security logic here means the rest of the application
never needs to know HOW passwords are hashed or HOW tokens are signed.

How JWT works:
  1. On login, we create a token that contains the user's ID as the "sub" claim.
  2. The token is signed with JWT_SECRET_KEY — tampering invalidates the signature.
  3. On every protected request, we decode the token and look up the user.
  4. The token expires after ACCESS_TOKEN_EXPIRE_MINUTES.
"""
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from app.core.config import settings


# ──────────────────────────────────────────────
# Password helpers
# ──────────────────────────────────────────────

def hash_password(plain_password: str) -> str:
    """Return bcrypt hash of the plain-text password."""
    # Truncate to 72 bytes as per bcrypt specification
    pw_bytes = plain_password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if the plain password matches the stored hash."""
    try:
        pw_bytes = plain_password.encode("utf-8")[:72]
        return bcrypt.checkpw(pw_bytes, hashed_password.encode("utf-8"))
    except Exception:
        return False


# ──────────────────────────────────────────────
# JWT helpers
# ──────────────────────────────────────────────

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT.

    :param subject: Typically the user's ID as a string.
    :param expires_delta: Override default expiry.
    :return: Encoded JWT string.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": str(subject),   # subject — who the token belongs to
        "exp": expire,         # expiry — token becomes invalid after this
        "iat": datetime.now(timezone.utc),  # issued-at
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """
    Decode and verify a JWT, returning the subject (user ID) or None.

    Returns None instead of raising so callers decide how to handle it.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload.get("sub")
    except JWTError:
        return None
