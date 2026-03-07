from fastapi import APIRouter, Depends, status
from app.services.notehandler import NoteManager
from app.config.dependencies import get_current_user, get_admin_user
from app.models import schemas

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=schemas.UserResponseModel, status_code=status.HTTP_201_CREATED)
async def create_note(request: schemas.NoteCreate, email: str = Depends(get_current_user)):
    return await NoteManager.create_note(request, email)

@router.get("/", response_model=schemas.UserResponseModel)
async def get_my_notes(email: str = Depends(get_current_user)):
    return await NoteManager.get_notes(email)

@router.get("/all", response_model=schemas.UserResponseModel)
async def get_all_notes(admin_user: dict = Depends(get_admin_user)):
    return await NoteManager.get_all_notes()
