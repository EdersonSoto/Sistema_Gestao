from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import time
from dataclasses import dataclass


HASH_ITERATIONS = 210000
TOKEN_TTL_SECONDS = 60 * 60 * 8
SECRET_KEY = "dev-secret-change-me"


def hash_password(password: str, salt: str | None = None) -> str:
    salt_bytes = base64.urlsafe_b64decode(salt.encode()) if salt else secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, HASH_ITERATIONS)
    return f"pbkdf2_sha256${HASH_ITERATIONS}${base64.urlsafe_b64encode(salt_bytes).decode()}${base64.urlsafe_b64encode(derived).decode()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt, digest = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        candidate = hash_password(password, salt=salt)
        return hmac.compare_digest(candidate, stored_hash)
    except ValueError:
        return False


def create_token(subject: str) -> str:
    issued_at = str(int(time.time()))
    payload = f"{subject}:{issued_at}"
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).digest()
    token = f"{payload}:{base64.urlsafe_b64encode(signature).decode()}"
    return base64.urlsafe_b64encode(token.encode()).decode()


@dataclass(frozen=True)
class TokenData:
    subject: str
    issued_at: int


def decode_token(token: str) -> TokenData | None:
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        subject, issued_at_raw, signature = decoded.rsplit(":", 2)
        payload = f"{subject}:{issued_at_raw}"
        expected = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(base64.urlsafe_b64encode(expected).decode(), signature):
            return None
        issued_at = int(issued_at_raw)
        if time.time() - issued_at > TOKEN_TTL_SECONDS:
            return None
        return TokenData(subject=subject, issued_at=issued_at)
    except (ValueError, UnicodeDecodeError, base64.binascii.Error):
        return None
