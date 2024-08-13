from fastapi import APIRouter, HTTPException, Depends , Request , Form , Header
from typing import List , Dict , Any ,Optional
from src.core.db import get_collection
from src.services.user.crud_user import UserService
from src.services.user.schema import UserCreate, UserResponse
from src.services.user.crud_user import UserService
from src.services.user.auth import decode_jwt_token

router = APIRouter()

# Dependency
def get_user_service() -> UserService:
    collection = get_collection("users")
    return UserService(collection=collection)

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user)

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: str, service: UserService = Depends(get_user_service)):
    return service.get_user(user_id)

@router.get("/users/", response_model=List[UserResponse])
def read_users(service: UserService = Depends(get_user_service)):
    users = service.find_all_users()
    return [UserResponse(id=str(user["_id"]), **user) for user in users]


@router.post("/token/", summary="Authenticate user and return JWT token")
async def login(
    email: str = Form(..., description="User email address"),
    password: str = Form(..., description="User password"),
    service: UserService = Depends(get_user_service)
) -> dict:
    """
    Authenticate a user using email and password, and return a JWT token if successful.

    Args:
        email (str): The user's email address.
        password (str): The user's password.
        service (UserService): The service used to authenticate the user.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If authentication fails, returns a 401 error.
    """
    token = service.authenticate_user(email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}


## this endpoint need to review 
from bson import ObjectId  # Import ObjectId for validation
@router.get("/users/me")
async def get_current_user(
    authorization: Optional[str] = Header(None),
    service: UserService = Depends(get_user_service)
) -> dict:
    """
    Retrieve the current user based on the JWT token provided in the Authorization header.

    Args:
        authorization (Optional[str]): The Authorization header containing the Bearer token.

    Returns:
        dict: A dictionary with the user ID if the token is valid.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        # Extract token from "Bearer <token>"
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    user_id = decode_jwt_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Validate ObjectId format
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    # Ensure user exists
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"user_id": user_id}


@router.delete("/users/{user_id}", response_model=Dict[str, Any])
def read_user(user_id: str, service: UserService = Depends(get_user_service)):
    deleted_user=service.delete_user(user_id)
    return {
        "detail": "User deleted successfully",
        "user": deleted_user
    }

