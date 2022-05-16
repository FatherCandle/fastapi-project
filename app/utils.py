from passlib.context import CryptContext

# Setting an hashing algorithem to use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(passowrd: str):
    return pwd_context.hash(passowrd)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
