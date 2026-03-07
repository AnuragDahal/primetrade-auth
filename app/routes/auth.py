from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status
from app.services.authhandler import AuthHandler
from app.models import schemas

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponseModel)
async def userSignup(request: schemas.UserCreate):
    new_user = await AuthHandler.handleSignUp(request)
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.UserResponseModel)
async def userLogin(request: OAuth2PasswordRequestForm = Depends()):
    user = await AuthHandler.handleLogin(request)
    return user
