from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
import jwt

from fastapi import Depends ,Header , HTTPException
from datetime import datetime, timedelta, timezone


import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM =  os.getenv("ALGORITHM")

def password_hash(password:str ):
    pwd = PasswordHash([Argon2Hasher()])

    hash =  pwd.hash(password)
    return hash

def verify_hash(password:str , hash: str ):
    pwd = PasswordHash([Argon2Hasher()])

    return pwd.verify(password , hash)


def create_access_token(user_id: int , username:str ):
    payload = {
        "sub": str(user_id),
        "user_name":username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )



def get_current_user(Auth2PasswordBearer: str = Header()):

    try:
        payload = jwt.decode(
            Auth2PasswordBearer,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return int(user_id)

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )



