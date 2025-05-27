import pytest
from bson import ObjectId
from datetime import datetime, timezone
from app.schemas.company import (
    create_company, get_company_by_id, get_companies_by_admin, 
    get_all_companies, update_company, delete_company
)
from app.models.company import CompanyCreate


@pytest.mark.asyncio
class TestCompanySchemas:
    """Test company database schema operations."""

    async def test_create_company(self, test_db, sample_company_data):
        """Test creating a company in the database."""
        company_create = CompanyCreate(**sample_company_data)
        
        company_id = await create_company(test_db, company_create)
        
        assert company_id is not None
        assert ObjectId.is_valid(company_id)

    async def test_create_company_sets_created_at(self, test_db, sample_company_data):
        """Test that created_at is automatically set when creating a company."""
        company_create = CompanyCreate(**sample_company_data)
        
        company_id = await create_company(test_db, company_create)
        
        company = await get_company_by_id(test_db, company_id)
        # Just verify that created_at is set and is a datetime object
        assert company.created_at is not None
        assert isinstance(company.created_at, datetime)

    async def test_get_company_by_id(self, test_db, sample_company_data):
        """Test retrieving a company by ID."""
        company_create = CompanyCreate(**sample_company_data)
        
        company_id = await create_company(test_db, company_create)
        company = await get_company_by_id(test_db, company_id)
        
        assert company is not None
        assert company.id == company_id
        assert company.name == sample_company_data["name"]
        assert company.description == sample_company_data["description"]
        assert company.admin_id == sample_company_data["admin_id"]
        assert isinstance(company.created_at, datetime)

    async def test_get_company_by_id_not_found(self, test_db):
        """Test retrieving a non-existent company by ID."""
        fake_id = str(ObjectId())
        company = await get_company_by_id(test_db, fake_id)
        
        assert company is None

    async def test_get_company_by_id_invalid_id(self, test_db):
        """Test retrieving a company with invalid ID format."""
        with pytest.raises(Exception):
            await get_company_by_id(test_db, "invalid_id")

    async def test_get_companies_by_admin(self, test_db):
        """Test retrieving companies by admin ID."""
        admin_id = "507f1f77bcf86cd799439011"
        
        # Create multiple companies for the same admin
        company_data1 = {
            "name": "Cafe 1",
            "description": "First cafe",
            "admin_id": admin_id
        }
        company_data2 = {
            "name": "Cafe 2",
            "description": "Second cafe",
            "admin_id": admin_id
        }
        
        company_create1 = CompanyCreate(**company_data1)
        company_create2 = CompanyCreate(**company_data2)
        
        company_id1 = await create_company(test_db, company_create1)
        company_id2 = await create_company(test_db, company_create2)
        
        companies = await get_companies_by_admin(test_db, admin_id)
        
        assert len(companies) == 2
        company_ids = [company.id for company in companies]
        assert company_id1 in company_ids
        assert company_id2 in company_ids
        
        for company in companies:
            assert company.admin_id == admin_id

    async def test_get_companies_by_admin_no_companies(self, test_db):
        """Test retrieving companies for admin with no companies."""
        admin_id = "507f1f77bcf86cd799439999"
        
        companies = await get_companies_by_admin(test_db, admin_id)
        
        assert len(companies) == 0

    async def test_get_all_companies(self, test_db):
        """Test retrieving all companies."""
        # Create companies for different admins
        company_data1 = {
            "name": "Cafe A",
            "admin_id": "507f1f77bcf86cd799439011"
        }
        company_data2 = {
            "name": "Cafe B", 
            "admin_id": "507f1f77bcf86cd799439022"
        }
        
        company_create1 = CompanyCreate(**company_data1)
        company_create2 = CompanyCreate(**company_data2)
        
        company_id1 = await create_company(test_db, company_create1)
        company_id2 = await create_company(test_db, company_create2)
        
        companies = await get_all_companies(test_db)
        
        assert len(companies) >= 2
        company_ids = [company.id for company in companies]
        assert company_id1 in company_ids
        assert company_id2 in company_ids

    async def test_get_all_companies_empty(self, test_db):
        """Test retrieving all companies when none exist."""
        companies = await get_all_companies(test_db)
        
        assert len(companies) == 0

    async def test_update_company(self, test_db, sample_company_data):
        """Test updating company data."""
        company_create = CompanyCreate(**sample_company_data)
        
        company_id = await create_company(test_db, company_create)
        
        update_data = {
            "name": "Updated Cafe Name",
            "description": "Updated description"
        }
        result = await update_company(test_db, company_id, update_data)
        
        assert result is True
        
        updated_company = await get_company_by_id(test_db, company_id)
        assert updated_company.name == "Updated Cafe Name"
        assert updated_company.description == "Updated description"
        assert updated_company.admin_id == sample_company_data["admin_id"]

    async def test_update_company_not_found(self, test_db):
        """Test updating a non-existent company."""
        fake_id = str(ObjectId())
        update_data = {"name": "Updated Name"}
        
        result = await update_company(test_db, fake_id, update_data)
        
        assert result is False

    async def test_update_company_invalid_id(self, test_db):
        """Test updating a company with invalid ID format."""
        update_data = {"name": "Updated Name"}
        
        with pytest.raises(Exception):
            await update_company(test_db, "invalid_id", update_data)

    async def test_delete_company(self, test_db, sample_company_data):
        """Test deleting a company."""
        company_create = CompanyCreate(**sample_company_data)
        
        company_id = await create_company(test_db, company_create)
        result = await delete_company(test_db, company_id)
        
        assert result is True
        
        deleted_company = await get_company_by_id(test_db, company_id)
        assert deleted_company is None

    async def test_delete_company_not_found(self, test_db):
        """Test deleting a non-existent company."""
        fake_id = str(ObjectId())
        result = await delete_company(test_db, fake_id)
        
        assert result is False

    async def test_delete_company_invalid_id(self, test_db):
        """Test deleting a company with invalid ID format."""
        with pytest.raises(Exception):
            await delete_company(test_db, "invalid_id")

    async def test_company_without_description(self, test_db):
        """Test creating a company without description."""
        company_data = {
            "name": "Simple Cafe",
            "admin_id": "507f1f77bcf86cd799439011"
        }
        company_create = CompanyCreate(**company_data)
        
        company_id = await create_company(test_db, company_create)
        company = await get_company_by_id(test_db, company_id)
        
        assert company.name == "Simple Cafe"
        assert company.description is None
        assert company.admin_id == "507f1f77bcf86cd799439011"