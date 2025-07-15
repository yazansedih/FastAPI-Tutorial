from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.users_db import users
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Change this line - use HTTPBearer instead of OAuth2PasswordBearer
security = HTTPBearer()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Modified get_current_user function
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in users:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ✅ Route: Signup
@router.post("/signup")
def signup(form: OAuth2PasswordRequestForm = Depends()):
    if form.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[form.username] = hash_password(form.password)
    return {"msg": "User created successfully"}

# ✅ Route: Login (returns JWT)
@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user_pass_hash = users.get(form.username)
    if not user_pass_hash or not verify_password(form.password, user_pass_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        
    access_token = create_access_token(data={"sub": form.username})
    return {"access_token": access_token, "token_type": "bearer"}