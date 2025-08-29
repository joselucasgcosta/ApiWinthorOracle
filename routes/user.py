from fastapi import APIRouter, Depends
from security.auth import get_current_user

router = APIRouter()

@router.get("/me")
async def read_users_me(user: dict = Depends(get_current_user)):
    return {
        "username": user["username"],
        "full_name": user["full_name"]
    }
