from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt(value):
    return pwd_context.hash(value)
