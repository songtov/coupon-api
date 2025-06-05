import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import Depends
from app.main import app
from app.models.user import User
from app.core.auth import create_access_token
from app.api.company import router
from datetime import datetime, timedelta
from bson import ObjectId

client = TestClient(app)

@pytest.fixture
def admin_user():
    """Create a sample admin user for testing."""
    return User(
        id="507f1f77bcf86cd799439011",
        email="admin@example.com",
        name="Admin User",
        role="admin"
    )

@pytest.fixture
def client_user():
    """Create a sample client user for testing."""
    return User(
        id="507f1f77bcf86cd799439012",
        email="client@example.com",
        name="Client User",
        role="client"
    )

@pytest.fixture
def admin_token(admin_user):
    """Create JWT token for admin user."""
    return create_access_token(
        data={"sub": admin_user.email, "role": admin_user.role},
        expires_delta=timedelta(minutes=30)
    )

@pytest.fixture
def client_token(client_user):
    """Create JWT token for client user."""
    return create_access_token(
        data={"sub": client_user.email, "role": client_user.role},
        expires_delta=timedelta(minutes=30)
    )

@pytest.fixture
def sample_company():
    """Sample company data."""
    return {
        "_id": ObjectId("507f1f77bcf86cd799439013"),
        "name": "Test Cafe",
        "description": "A test cafe",
        "admin_id": "507f1f77bcf86cd799439011",
        "created_at": datetime.utcnow()
    }

class TestCompanyAPI:
    """Test cases for Company API endpoints."""

    @pytest.mark.asyncio
    async def test_create_company_success(self, admin_user, admin_token):
        """Test successful company creation by admin."""
        from app.api.company import get_db, get_current_admin
        
        mock_db = AsyncMock()
        mock_db.companies.insert_one.return_value = AsyncMock(
            inserted_id=ObjectId("507f1f77bcf86cd799439013")
        )
        mock_db.companies.find_one.return_value = {
            "_id": ObjectId("507f1f77bcf86cd799439013"),
            "name": "Test Cafe",
            "description": "A test cafe",
            "admin_id": "507f1f77bcf86cd799439011",
            "created_at": datetime.utcnow()
        }

        # Override dependencies
        app.dependency_overrides[get_db] = lambda: mock_db
        app.dependency_overrides[get_current_admin] = lambda: admin_user
        
        try:
            response = client.post(
                "/api/companies/",
                json={
                    "name": "Test Cafe",
                    "description": "A test cafe"
                }
            )

            assert response.status_code == 201
            data = response.json()
            assert data["name"] == "Test Cafe"
            assert data["description"] == "A test cafe"
            assert data["admin_id"] == admin_user.id
        finally:
            # Clear overrides
            app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_create_company_unauthorized(self, client_token):
        """Test company creation fails for non-admin users."""
        response = client.post(
            "/api/companies/",
            json={
                "name": "Test Cafe",
                "description": "A test cafe"
            },
            headers={"Authorization": f"Bearer {client_token}"}
        )

        assert response.status_code == 403
        assert "Not enough permissions" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_create_company_no_auth(self):
        """Test company creation fails without authentication."""
        response = client.post(
            "/api/companies/",
            json={
                "name": "Test Cafe",
                "description": "A test cafe"
            }
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_list_companies_success(self, admin_user, admin_token, sample_company):
        """Test successful company listing."""
        mock_db = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor
        mock_cursor.to_list.return_value = [sample_company]
        mock_db.companies.find.return_value = mock_cursor

        with patch("app.api.company.get_db", return_value=mock_db), \
             patch("app.api.company.get_current_admin", return_value=admin_user):
            
            response = client.get(
                "/api/companies/",
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Cafe"
        assert data[0]["admin_id"] == admin_user.id

    @pytest.mark.asyncio
    async def test_list_companies_pagination(self, admin_user, admin_token):
        """Test company listing with pagination."""
        mock_db = AsyncMock()
        mock_cursor = AsyncMock()
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor
        mock_cursor.to_list.return_value = []
        mock_db.companies.find.return_value = mock_cursor

        with patch("app.api.company.get_db", return_value=mock_db), \
             patch("app.api.company.get_current_admin", return_value=admin_user):
            
            response = client.get(
                "/api/companies/?skip=10&limit=5",
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 200
        mock_cursor.skip.assert_called_with(10)
        mock_cursor.limit.assert_called_with(5)

    @pytest.mark.asyncio
    async def test_get_company_success(self, admin_user, admin_token, sample_company):
        """Test successful company retrieval."""
        mock_db = AsyncMock()
        mock_db.companies.find_one.return_value = sample_company

        with patch("app.api.company.get_db", return_value=mock_db), \
             patch("app.api.company.get_current_admin", return_value=admin_user):
            
            response = client.get(
                f"/api/companies/{sample_company['_id']}",
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Cafe"
        assert data["admin_id"] == admin_user.id

    @pytest.mark.asyncio
    async def test_get_company_not_found(self, admin_user, admin_token):
        """Test company retrieval with non-existent ID."""
        mock_db = AsyncMock()
        mock_db.companies.find_one.return_value = None

        with patch("app.api.company.get_db", return_value=mock_db), \
             patch("app.api.company.get_current_admin", return_value=admin_user):
            
            response = client.get(
                "/api/companies/507f1f77bcf86cd799439999",
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 404
        assert "Company not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_update_company_success(self, admin_user, admin_token, sample_company):
        """Test successful company update."""
        mock_db = AsyncMock()
        mock_db.companies.find_one.return_value = sample_company
        updated_company = sample_company.copy()
        updated_company["name"] = "Updated Cafe"
        mock_db.companies.find_one.side_effect = [sample_company, updated_company]

        with patch("app.api.company.get_db", return_value=mock_db), \
             patch("app.api.company.get_current_admin", return_value=admin_user):
            
            response = client.put(
                f"/api/companies/{sample_company['_id']}",
                json={
                    "name": "Updated Cafe",
                    "description": "Updated description"
                },
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Cafe"

    @pytest.mark.asyncio
    async def test_update_company_not_found(self, admin_user, admin_token):
        """Test company update with non-existent ID."""
        mock_db = AsyncMock()
        mock_db.companies.find_one.return_value = None

        with patch("app.api.company.get_db", return_value=mock_db), \
             patch("app.api.company.get_current_admin", return_value=admin_user):
            
            response = client.put(
                "/api/companies/507f1f77bcf86cd799439999",
                json={
                    "name": "Updated Cafe"
                },
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 404
        assert "Company not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_delete_company_success(self, admin_user, admin_token, sample_company):
        """Test successful company deletion."""
        mock_db = AsyncMock()
        mock_db.companies.find_one.return_value = sample_company

        with patch("app.api.company.get_db", return_value=mock_db), \
             patch("app.api.company.get_current_admin", return_value=admin_user):
            
            response = client.delete(
                f"/api/companies/{sample_company['_id']}",
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 204
        mock_db.companies.delete_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_company_not_found(self, admin_user, admin_token):
        """Test company deletion with non-existent ID."""
        mock_db = AsyncMock()
        mock_db.companies.find_one.return_value = None

        with patch("app.api.company.get_db", return_value=mock_db), \
             patch("app.api.company.get_current_admin", return_value=admin_user):
            
            response = client.delete(
                "/api/companies/507f1f77bcf86cd799439999",
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 404
        assert "Company not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_admin_isolation(self, admin_token):
        """Test that admins can only access their own companies."""
        # Create two different admin users
        admin1 = User(
            id="507f1f77bcf86cd799439011",
            email="admin1@example.com",
            name="Admin 1",
            role="admin"
        )
        admin2 = User(
            id="507f1f77bcf86cd799439012",
            email="admin2@example.com",
            name="Admin 2",
            role="admin"
        )
        
        # Company belongs to admin2
        other_admin_company = {
            "_id": ObjectId("507f1f77bcf86cd799439013"),
            "name": "Other Admin's Cafe",
            "admin_id": "507f1f77bcf86cd799439012",
            "created_at": datetime.utcnow()
        }

        mock_db = AsyncMock()
        mock_db.companies.find_one.return_value = None  # Admin1 can't see admin2's company

        with patch("app.api.company.get_db", return_value=mock_db), \
             patch("app.api.company.get_current_admin", return_value=admin1):
            
            response = client.get(
                f"/api/companies/{other_admin_company['_id']}",
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 404
        # Verify the query included admin_id filter
        mock_db.companies.find_one.assert_called_with({
            "_id": ObjectId(str(other_admin_company['_id'])),
            "admin_id": admin1.id
        })

    @pytest.mark.asyncio
    async def test_invalid_company_id_format(self, admin_user, admin_token):
        """Test handling of invalid ObjectId format."""
        mock_db = AsyncMock()

        with patch("app.api.company.get_db", return_value=mock_db), \
             patch("app.api.company.get_current_admin", return_value=admin_user):
            
            response = client.get(
                "/api/companies/invalid-id",
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        # Should return 422 for invalid ObjectId format
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_company_validation(self, admin_user, admin_token):
        """Test company creation with invalid data."""
        with patch("app.api.company.get_current_admin", return_value=admin_user):
            # Test empty name
            response = client.post(
                "/api/companies/",
                json={
                    "name": "",
                    "description": "Test description"
                },
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 422

        with patch("app.api.company.get_current_admin", return_value=admin_user):
            # Test missing required field
            response = client.post(
                "/api/companies/",
                json={
                    "description": "Test description"
                },
                headers={"Authorization": f"Bearer {admin_token}"}
            )

        assert response.status_code == 422