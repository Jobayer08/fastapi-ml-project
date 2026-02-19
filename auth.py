from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# SECRET
SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# FIXED hashed password (static)
fake_user = {
    "username": "jobayer",

    # password = 1234
    "password": "$2b$12$C/vZYyBo4hzhapRNtKlM3.aizARsPCUw/ESAJGSFXc7DJIa1NqGsK"
}


def verify_password(plain_password, hashed_password):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def authenticate_user(username, password):

    if username != fake_user["username"]:
        return False

    if not verify_password(
        password,
        fake_user["password"]
    ):
        return False

    return username


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
