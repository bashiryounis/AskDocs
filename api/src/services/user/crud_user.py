from pymongo.collection import Collection
from bson import ObjectId
from passlib.context import CryptContext
from src.services.user.schema import UserCreate, UserResponse
from datetime import datetime
from fastapi import HTTPException
from typing import Optional , List
from src.services.user.auth import create_jwt_token


class UserService:
    """
    Service class for managing user operations, including creation, retrieval,
    authentication, and deletion within a MongoDB collection.
    """

    def __init__(self, collection: Collection):
        self.collection = collection
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_user(self, user: UserCreate) -> UserResponse:
        """
        Create a new user, hashing their password and saving them in the database.

        Args:
            user (UserCreate): The user creation schema containing user data.

        Returns:
            UserResponse: The response model containing the created user's data.

        Raises:
            HTTPException: If the email is already registered.
        """
        existing_user = self.collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data = user.model_dump()
        user_data["password"] = self.hash_password(user_data["password"])
        user_data["created_at"] = datetime.now()
        user_data["updated_at"] = datetime.now()

        result = self.collection.insert_one(user_data)
        return UserResponse(id=str(result.inserted_id), **user_data)

    def get_user(self, user_id: str) -> UserResponse:
        """
        Retrieve a user's data by their unique ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            UserResponse: The response model containing the user's data.

        Raises:
            HTTPException: If the user is not found.
        """
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(id=str(user["_id"]), **user)
    def find_all_users(self) -> List[UserResponse]:
        """
        Retrieve a list of all users from the database.

        Returns:
            List[UserResponse]: A list of response models containing user data.
        """
        return list(self.collection.find())
    
    def delete_user(self, user_id: str) -> UserResponse:
        """
        Delete a user by their unique ID.

        Args:
            user_id (str): The ID of the user to remove.

        Returns:
            UserResponse: The response model containing the removed user's data.

        Raises:
            HTTPException: If the user is not found.
        """
        user = self.collection.find_one_and_delete({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(id=str(user["_id"]), **user)

    def authenticate_user(self, email: str, password: str) -> Optional[str]:
        """
        Authenticate a user by their email and password, returning a JWT token if successful.

        Args:
            email (str): The user's email address.
            password (str): The plain-text password to verify.

        Returns:
            Optional[str]: A JWT token if authentication is successful, otherwise None.
        """
        user = self.collection.find_one({"email": email})
        if user and self.verify_password(password, user['password']):
            return create_jwt_token(str(user["_id"]))
        return None
