from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_passwd(password: str):
    return pwd_context.hash(password)

def passwd_verify(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)
