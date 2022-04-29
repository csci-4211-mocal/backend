from typing import Optional
from datetime import datetime, timedelta

from fastapi.requests import Request
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError, JWTClaimsError
from passlib.context import CryptContext

secret_key = "supersecretkey"
method = "HS256"
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_token(account_id: str, expire: timedelta = timedelta(days=14)) -> Optional[str]:
    expire = datetime.utcnow() + expire
    claims = {
        "id": account_id,
        "exp": expire
    }

    try:
        encoded_jwt = jwt.encode(claims, secret_key, algorithm=method)
        return encoded_jwt

    except JWTError:
        print('Error generating token')
        return None


def extract_claims(token: str) -> dict:
    try:
        return jwt.decode(str(token), str(secret_key))

    except (JWTError, ExpiredSignatureError, JWTClaimsError) as e:
        print(f'Error verifying token: {e}')
        return None