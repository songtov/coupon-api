import pytest
from pydantic import ValidationError
from app.models.user import UserRole, UserBase, UserCreate, UserInDB, User


class TestUserModels:
    """Test user Pydantic models."""

    def test_user_role_enum(self):
        """Test UserRole enum values."""
        assert UserRole.ADMIN == "admin"
        assert UserRole.CLIENT == "client"

    def test_user_base_valid(self):
        """Test UserBase with valid data."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.ADMIN
        }
        user = UserBase(**user_data)
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == UserRole.ADMIN

    def test_user_base_invalid_email(self):
        """Test UserBase with invalid email."""
        user_data = {
            "email": "invalid-email",
            "name": "Test User",
            "role": UserRole.ADMIN
        }
        with pytest.raises(ValidationError):
            UserBase(**user_data)

    def test_user_base_invalid_role(self):
        """Test UserBase with invalid role."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "role": "invalid_role"
        }
        with pytest.raises(ValidationError):
            UserBase(**user_data)

    def test_user_base_missing_fields(self):
        """Test UserBase with missing required fields."""
        with pytest.raises(ValidationError):
            UserBase(email="test@example.com")

    def test_user_create_valid(self):
        """Test UserCreate with valid data."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.CLIENT,
            "password": "password123"
        }
        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == UserRole.CLIENT
        assert user.password == "password123"

    def test_user_create_missing_password(self):
        """Test UserCreate without password."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.CLIENT
        }
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_in_db_valid(self):
        """Test UserInDB with valid data."""
        user_data = {
            "_id": "507f1f77bcf86cd799439011",
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.ADMIN,
            "hashed_password": "hashed_password_123"
        }
        user = UserInDB(**user_data)
        assert user.id == "507f1f77bcf86cd799439011"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == UserRole.ADMIN
        assert user.hashed_password == "hashed_password_123"

    def test_user_in_db_alias_id(self):
        """Test UserInDB _id alias works correctly."""
        user_data = {
            "_id": "507f1f77bcf86cd799439011",
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.ADMIN,
            "hashed_password": "hashed_password_123"
        }
        user = UserInDB(**user_data)
        assert user.id == "507f1f77bcf86cd799439011"

    def test_user_valid(self):
        """Test User model with valid data."""
        user_data = {
            "id": "507f1f77bcf86cd799439011",
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.CLIENT
        }
        user = User(**user_data)
        assert user.id == "507f1f77bcf86cd799439011"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == UserRole.CLIENT

    def test_user_missing_id(self):
        """Test User model without id."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.CLIENT
        }
        with pytest.raises(ValidationError):
            User(**user_data)

    def test_user_serialization(self):
        """Test user model serialization."""
        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.ADMIN,
            "password": "password123"
        }
        user = UserCreate(**user_data)
        user_dict = user.dict()
        assert user_dict["email"] == "test@example.com"
        assert user_dict["role"] == "admin"

    def test_user_json_serialization(self):
        """Test user model JSON serialization."""
        user_data = {
            "id": "507f1f77bcf86cd799439011",
            "email": "test@example.com",
            "name": "Test User",
            "role": UserRole.CLIENT
        }
        user = User(**user_data)
        user_json = user.json()
        assert '"email":"test@example.com"' in user_json
        assert '"role":"client"' in user_json