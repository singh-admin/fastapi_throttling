import hashlib
import hmac
import os
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv


# Load .env variables
load_dotenv()

# .env settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

#-------------------------------------- Hashing Algorithm ----------------------------------------------------#

def hash_password(password: str) -> str:
    """Hash a password using HMAC with SHA-256."""
    password = password.encode("utf-8")
    return hmac.new(SECRET_KEY.encode("utf-8"), password, hashlib.sha256).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password by comparing it to its hashed version."""
    return hmac.compare_digest(hash_password(plain_password), hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
