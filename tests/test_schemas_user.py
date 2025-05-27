import pytest
from bson import ObjectId
from app.schemas.user import (
    create_user, get_user_by_id, get_user_by_email, 
    update_user, delete_user
)
from app.models.user import UserCreate, UserRole


@pytest.mark.asyncio
class TestUserSchemas:
    """Test user database schema operations."""

    async def test_create_user(self, test_db, sample_user_data):
        """Test creating a user in the database."""
        user_create = UserCreate(**sample_user_data)
        hashed_password = "hashed_password_123"
        
        user_id = await create_user(test_db, user_create, hashed_password)
        
        assert user_id is not None
        assert ObjectId.is_valid(user_id)

    async def test_get_user_by_id(self, test_db, sample_user_data):
        """Test retrieving a user by ID."""
        user_create = UserCreate(**sample_user_data)
        hashed_password = "hashed_password_123"
        
        user_id = await create_user(test_db, user_create, hashed_password)
        user = await get_user_by_id(test_db, user_id)
        
        assert user is not None
        assert user.id == user_id
        assert user.email == sample_user_data["email"]
        assert user.name == sample_user_data["name"]
        assert user.role == sample_user_data["role"]
        assert user.hashed_password == hashed_password

    async def test_get_user_by_id_not_found(self, test_db):
        """Test retrieving a non-existent user by ID."""
        fake_id = str(ObjectId())
        user = await get_user_by_id(test_db, fake_id)
        
        assert user is None

    async def test_get_user_by_id_invalid_id(self, test_db):
        """Test retrieving a user with invalid ID format."""
        with pytest.raises(Exception):
            await get_user_by_id(test_db, "invalid_id")

    async def test_get_user_by_email(self, test_db, sample_user_data):
        """Test retrieving a user by email."""
        user_create = UserCreate(**sample_user_data)
        hashed_password = "hashed_password_123"
        
        user_id = await create_user(test_db, user_create, hashed_password)
        user = await get_user_by_email(test_db, sample_user_data["email"])
        
        assert user is not None
        assert user.id == user_id
        assert user.email == sample_user_data["email"]
        assert user.name == sample_user_data["name"]
        assert user.role == sample_user_data["role"]

    async def test_get_user_by_email_not_found(self, test_db):
        """Test retrieving a non-existent user by email."""
        user = await get_user_by_email(test_db, "nonexistent@example.com")
        
        assert user is None

    async def test_update_user(self, test_db, sample_user_data):
        """Test updating user data."""
        user_create = UserCreate(**sample_user_data)
        hashed_password = "hashed_password_123"
        
        user_id = await create_user(test_db, user_create, hashed_password)
        
        update_data = {"name": "Updated Name", "role": UserRole.CLIENT}
        result = await update_user(test_db, user_id, update_data)
        
        assert result is True
        
        updated_user = await get_user_by_id(test_db, user_id)
        assert updated_user.name == "Updated Name"
        assert updated_user.role == UserRole.CLIENT
        assert updated_user.email == sample_user_data["email"]

    async def test_update_user_not_found(self, test_db):
        """Test updating a non-existent user."""
        fake_id = str(ObjectId())
        update_data = {"name": "Updated Name"}
        
        result = await update_user(test_db, fake_id, update_data)
        
        assert result is False

    async def test_update_user_invalid_id(self, test_db):
        """Test updating a user with invalid ID format."""
        update_data = {"name": "Updated Name"}
        
        with pytest.raises(Exception):
            await update_user(test_db, "invalid_id", update_data)

    async def test_delete_user(self, test_db, sample_user_data):
        """Test deleting a user."""
        user_create = UserCreate(**sample_user_data)
        hashed_password = "hashed_password_123"
        
        user_id = await create_user(test_db, user_create, hashed_password)
        result = await delete_user(test_db, user_id)
        
        assert result is True
        
        deleted_user = await get_user_by_id(test_db, user_id)
        assert deleted_user is None

    async def test_delete_user_not_found(self, test_db):
        """Test deleting a non-existent user."""
        fake_id = str(ObjectId())
        result = await delete_user(test_db, fake_id)
        
        assert result is False

    async def test_delete_user_invalid_id(self, test_db):
        """Test deleting a user with invalid ID format."""
        with pytest.raises(Exception):
            await delete_user(test_db, "invalid_id")

    async def test_create_multiple_users_same_email(self, test_db, sample_user_data):
        """Test creating multiple users with the same email should work (no unique constraint in this implementation)."""
        user_create = UserCreate(**sample_user_data)
        hashed_password = "hashed_password_123"
        
        user_id1 = await create_user(test_db, user_create, hashed_password)
        user_id2 = await create_user(test_db, user_create, hashed_password)
        
        assert user_id1 != user_id2
        assert ObjectId.is_valid(user_id1)
        assert ObjectId.is_valid(user_id2)

    async def test_user_password_not_stored_in_create(self, test_db, sample_user_data):
        """Test that the plain password is not stored in the database."""
        user_create = UserCreate(**sample_user_data)
        hashed_password = "hashed_password_123"
        
        user_id = await create_user(test_db, user_create, hashed_password)
        user = await get_user_by_id(test_db, user_id)
        
        assert user.hashed_password == hashed_password
        assert not hasattr(user, 'password')
        
        # Check that the original password is not in the database document
        user_doc = await test_db.users.find_one({"_id": ObjectId(user_id)})
        assert "password" not in user_doc
        assert user_doc["hashed_password"] == hashed_password