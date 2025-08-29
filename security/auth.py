from datetime import datetime, timedelta
from environment.config import ConfigAuth
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


# Configurações
SECRET_KEY = ConfigAuth.SECRET_KEY
ALGORITHM = ConfigAuth.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(ConfigAuth.ACCESS_TOKEN_EXPIRE_MINUTES)
<<<<<<< HEAD
=======
USER_1_USERNAME = ConfigAuth.USER_1_USERNAME
USER_1_PASSWORD = ConfigAuth.USER_1_PASSWORD
USER_1_USERNAME = ConfigAuth.USER_1_FULLNAME
>>>>>>> d623871 (Update version files)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

<<<<<<< HEAD
=======
<<<<<<< HEAD
password_jose = pwd_context.hash(USER_1_PASSWORD)
users_db = {
    "joselucas": {
        "username": USER_1_USERNAME,
        "full_name": USER_1_USERNAME,
=======
>>>>>>> d623871 (Update version files)
password_jose = pwd_context.hash("test$$password")
users_db = {
    "joselucas": {
        "username": "testuser",
        "full_name": "João da Silva Santos",
<<<<<<< HEAD
=======
>>>>>>> 6cd3a60aad58a544ee87743d4f2dbb440c0e5a62
>>>>>>> d623871 (Update version files)
        "hashed_password": password_jose,
        "role": "admin",
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    return db.get(username)

def authenticate_user(username: str, password: str):
    user = get_user(users_db, username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user(users_db, username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
