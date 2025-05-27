import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.company import CompanyBase, CompanyCreate, CompanyInDB, Company


class TestCompanyModels:
    """Test company Pydantic models."""

    def test_company_base_valid(self):
        """Test CompanyBase with valid data."""
        company_data = {
            "name": "Test Cafe",
            "description": "A test cafe for testing"
        }
        company = CompanyBase(**company_data)
        assert company.name == "Test Cafe"
        assert company.description == "A test cafe for testing"

    def test_company_base_optional_description(self):
        """Test CompanyBase with optional description."""
        company_data = {
            "name": "Test Cafe"
        }
        company = CompanyBase(**company_data)
        assert company.name == "Test Cafe"
        assert company.description is None

    def test_company_base_missing_name(self):
        """Test CompanyBase with missing required name."""
        company_data = {
            "description": "A test cafe for testing"
        }
        with pytest.raises(ValidationError):
            CompanyBase(**company_data)

    def test_company_base_empty_name(self):
        """Test CompanyBase with empty name."""
        company_data = {
            "name": "",
            "description": "A test cafe for testing"
        }
        company = CompanyBase(**company_data)
        assert company.name == ""

    def test_company_create_valid(self):
        """Test CompanyCreate with valid data."""
        company_data = {
            "name": "Test Cafe",
            "description": "A test cafe for testing",
            "admin_id": "507f1f77bcf86cd799439011"
        }
        company = CompanyCreate(**company_data)
        assert company.name == "Test Cafe"
        assert company.description == "A test cafe for testing"
        assert company.admin_id == "507f1f77bcf86cd799439011"

    def test_company_create_missing_admin_id(self):
        """Test CompanyCreate with missing admin_id."""
        company_data = {
            "name": "Test Cafe",
            "description": "A test cafe for testing"
        }
        with pytest.raises(ValidationError):
            CompanyCreate(**company_data)

    def test_company_in_db_valid(self):
        """Test CompanyInDB with valid data."""
        created_at = datetime.utcnow()
        company_data = {
            "_id": "507f1f77bcf86cd799439012",
            "name": "Test Cafe",
            "description": "A test cafe for testing",
            "admin_id": "507f1f77bcf86cd799439011",
            "created_at": created_at
        }
        company = CompanyInDB(**company_data)
        assert company.id == "507f1f77bcf86cd799439012"
        assert company.name == "Test Cafe"
        assert company.description == "A test cafe for testing"
        assert company.admin_id == "507f1f77bcf86cd799439011"
        assert company.created_at == created_at

    def test_company_in_db_alias_id(self):
        """Test CompanyInDB _id alias works correctly."""
        created_at = datetime.utcnow()
        company_data = {
            "_id": "507f1f77bcf86cd799439012",
            "name": "Test Cafe",
            "admin_id": "507f1f77bcf86cd799439011",
            "created_at": created_at
        }
        company = CompanyInDB(**company_data)
        assert company.id == "507f1f77bcf86cd799439012"

    def test_company_in_db_missing_created_at(self):
        """Test CompanyInDB with missing created_at."""
        company_data = {
            "_id": "507f1f77bcf86cd799439012",
            "name": "Test Cafe",
            "admin_id": "507f1f77bcf86cd799439011"
        }
        with pytest.raises(ValidationError):
            CompanyInDB(**company_data)

    def test_company_valid(self):
        """Test Company model with valid data."""
        company_data = {
            "id": "507f1f77bcf86cd799439012",
            "name": "Test Cafe",
            "description": "A test cafe for testing",
            "admin_id": "507f1f77bcf86cd799439011"
        }
        company = Company(**company_data)
        assert company.id == "507f1f77bcf86cd799439012"
        assert company.name == "Test Cafe"
        assert company.description == "A test cafe for testing"
        assert company.admin_id == "507f1f77bcf86cd799439011"

    def test_company_missing_id(self):
        """Test Company model without id."""
        company_data = {
            "name": "Test Cafe",
            "admin_id": "507f1f77bcf86cd799439011"
        }
        with pytest.raises(ValidationError):
            Company(**company_data)

    def test_company_missing_admin_id(self):
        """Test Company model without admin_id."""
        company_data = {
            "id": "507f1f77bcf86cd799439012",
            "name": "Test Cafe"
        }
        with pytest.raises(ValidationError):
            Company(**company_data)

    def test_company_serialization(self):
        """Test company model serialization."""
        company_data = {
            "name": "Test Cafe",
            "description": "A test cafe for testing",
            "admin_id": "507f1f77bcf86cd799439011"
        }
        company = CompanyCreate(**company_data)
        company_dict = company.dict()
        assert company_dict["name"] == "Test Cafe"
        assert company_dict["description"] == "A test cafe for testing"
        assert company_dict["admin_id"] == "507f1f77bcf86cd799439011"

    def test_company_json_serialization(self):
        """Test company model JSON serialization."""
        company_data = {
            "id": "507f1f77bcf86cd799439012",
            "name": "Test Cafe",
            "admin_id": "507f1f77bcf86cd799439011"
        }
        company = Company(**company_data)
        company_json = company.json()
        assert '"name":"Test Cafe"' in company_json
        assert '"id":"507f1f77bcf86cd799439012"' in company_json