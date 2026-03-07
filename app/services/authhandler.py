from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.utils.response import send_response
from app.services.errorhandlers import ErrorHandler
from app.utils.jwtutil import create_access_token
from app.utils.passhashutils import Encrypt
from app.config.database import user_collection
from app.models import schemas
from app.config.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_DAYS = settings.ACCESS_TOKEN_EXPIRE_DAYS
TOKEN_TYPE = settings.TOKEN_TYPE
TOKEN_KEY = settings.TOKEN_KEY


class Validate:
    @staticmethod
    async def verify_email(email: str):
        check_email = await user_collection.find_one({"email": email})
        if check_email:
            return True
        return False


class AuthHandler:
    @staticmethod
    async def handleSignUp(request: schemas.UserCreate):
        duplicate_user = await Validate.verify_email(request.email)
        if duplicate_user:
            raise ErrorHandler.ALreadyExists("User already exists")
        hashed_password = Encrypt.hash_password(request.password)
        user_data = {
            **request.model_dump(exclude={"password"}), "password": hashed_password, "isEmailVerified": False}
        await user_collection.insert_one(user_data)
        return send_response(message="User created successfully")

    @staticmethod
    async def handleLogin(request: OAuth2PasswordRequestForm = Depends()):
        user = await user_collection.find_one({"email": request.username})
        if user:
            if not Encrypt.verify_password(request.password, user["password"]):
                raise ErrorHandler.Unauthorized("Incorrect email or password")
            access_token_expires = timedelta(
                days=ACCESS_TOKEN_EXPIRE_DAYS)
            access_token = create_access_token(
                data={"sub": user["email"]}, expires_delta=access_token_expires)
            return send_response(message="User Login SuccessFully", data={"access_token": access_token, "token_type": TOKEN_TYPE})
        raise ErrorHandler.NotFound("User not found")
