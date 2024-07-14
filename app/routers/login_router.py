from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta
from config.JWTUtility import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from interfaces.usecases.user_usecase_interface import UserUseCaseInterface
from entities.user import User
from schemas.UserSchema import UserSchema

class LoginRest:
    def __init__(self, user_usecase: UserUseCaseInterface):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.user_usecase = user_usecase
    
    def add_routes(self, router: APIRouter):
        router.post("/login", response_model=dict, tags=["login"])(self.login_for_access_token)
        router.post("/register-admin", response_model=dict, tags=["login"])(self.register_admin_user)

    def authenticate_user(self, username: str, password: str):
        user = self.user_usecase.get_user(username)
        if not user:
            return False
        if not self.pwd_context.verify(password, user.password):
            return False
        return user
    
    async def login_for_access_token(self, form_data: UserSchema):
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def register_admin_user(self, form_data: UserSchema):
        hashed_password = self.pwd_context.hash(form_data.password)
        admin_user = User(username=form_data.username, password=hashed_password, role="ADMIN")
        self.user_usecase.add_user(admin_user)
        return {"message": "Admin user registered successfully"}
