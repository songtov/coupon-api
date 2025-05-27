import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.coupon import CouponBase, CouponCreate, CouponInDB, Coupon


class TestCouponModels:
    """Test coupon Pydantic models."""

    def test_coupon_base_valid(self):
        """Test CouponBase with valid data."""
        coupon_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "123456789012"
        }
        coupon = CouponBase(**coupon_data)
        assert coupon.company_id == "507f1f77bcf86cd799439012"
        assert coupon.barcode == "123456789012"

    def test_coupon_base_missing_company_id(self):
        """Test CouponBase with missing company_id."""
        coupon_data = {
            "barcode": "123456789012"
        }
        with pytest.raises(ValidationError):
            CouponBase(**coupon_data)

    def test_coupon_base_missing_barcode(self):
        """Test CouponBase with missing barcode."""
        coupon_data = {
            "company_id": "507f1f77bcf86cd799439012"
        }
        with pytest.raises(ValidationError):
            CouponBase(**coupon_data)

    def test_coupon_base_empty_barcode(self):
        """Test CouponBase with empty barcode."""
        coupon_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": ""
        }
        coupon = CouponBase(**coupon_data)
        assert coupon.barcode == ""

    def test_coupon_create_valid(self):
        """Test CouponCreate with valid data."""
        coupon_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "987654321098"
        }
        coupon = CouponCreate(**coupon_data)
        assert coupon.company_id == "507f1f77bcf86cd799439012"
        assert coupon.barcode == "987654321098"

    def test_coupon_in_db_valid(self):
        """Test CouponInDB with valid data."""
        created_at = datetime.utcnow()
        updated_at = datetime.utcnow()
        coupon_data = {
            "_id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "555666777888",
            "client_id": "507f1f77bcf86cd799439011",
            "count": 5,
            "created_at": created_at,
            "updated_at": updated_at
        }
        coupon = CouponInDB(**coupon_data)
        assert coupon.id == "507f1f77bcf86cd799439014"
        assert coupon.company_id == "507f1f77bcf86cd799439012"
        assert coupon.barcode == "555666777888"
        assert coupon.client_id == "507f1f77bcf86cd799439011"
        assert coupon.count == 5
        assert coupon.created_at == created_at
        assert coupon.updated_at == updated_at

    def test_coupon_in_db_default_count(self):
        """Test CouponInDB with default count value."""
        created_at = datetime.utcnow()
        updated_at = datetime.utcnow()
        coupon_data = {
            "_id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "555666777888",
            "client_id": "507f1f77bcf86cd799439011",
            "created_at": created_at,
            "updated_at": updated_at
        }
        coupon = CouponInDB(**coupon_data)
        assert coupon.count == 0

    def test_coupon_in_db_alias_id(self):
        """Test CouponInDB _id alias works correctly."""
        created_at = datetime.utcnow()
        updated_at = datetime.utcnow()
        coupon_data = {
            "_id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "555666777888",
            "client_id": "507f1f77bcf86cd799439011",
            "created_at": created_at,
            "updated_at": updated_at
        }
        coupon = CouponInDB(**coupon_data)
        assert coupon.id == "507f1f77bcf86cd799439014"

    def test_coupon_in_db_missing_client_id(self):
        """Test CouponInDB with missing client_id."""
        created_at = datetime.utcnow()
        updated_at = datetime.utcnow()
        coupon_data = {
            "_id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "555666777888",
            "created_at": created_at,
            "updated_at": updated_at
        }
        with pytest.raises(ValidationError):
            CouponInDB(**coupon_data)

    def test_coupon_in_db_missing_timestamps(self):
        """Test CouponInDB with missing timestamps."""
        coupon_data = {
            "_id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "555666777888",
            "client_id": "507f1f77bcf86cd799439011"
        }
        with pytest.raises(ValidationError):
            CouponInDB(**coupon_data)

    def test_coupon_valid(self):
        """Test Coupon model with valid data."""
        coupon_data = {
            "id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "111222333444",
            "client_id": "507f1f77bcf86cd799439011",
            "count": 3
        }
        coupon = Coupon(**coupon_data)
        assert coupon.id == "507f1f77bcf86cd799439014"
        assert coupon.company_id == "507f1f77bcf86cd799439012"
        assert coupon.barcode == "111222333444"
        assert coupon.client_id == "507f1f77bcf86cd799439011"
        assert coupon.count == 3

    def test_coupon_missing_id(self):
        """Test Coupon model without id."""
        coupon_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "111222333444",
            "client_id": "507f1f77bcf86cd799439011",
            "count": 3
        }
        with pytest.raises(ValidationError):
            Coupon(**coupon_data)

    def test_coupon_missing_client_id(self):
        """Test Coupon model without client_id."""
        coupon_data = {
            "id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "111222333444",
            "count": 3
        }
        with pytest.raises(ValidationError):
            Coupon(**coupon_data)

    def test_coupon_missing_count(self):
        """Test Coupon model without count."""
        coupon_data = {
            "id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "111222333444",
            "client_id": "507f1f77bcf86cd799439011"
        }
        with pytest.raises(ValidationError):
            Coupon(**coupon_data)

    def test_coupon_invalid_count_type(self):
        """Test Coupon model with invalid count type."""
        coupon_data = {
            "id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "111222333444",
            "client_id": "507f1f77bcf86cd799439011",
            "count": "three"
        }
        with pytest.raises(ValidationError):
            Coupon(**coupon_data)

    def test_coupon_negative_count(self):
        """Test Coupon model with negative count."""
        coupon_data = {
            "id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "111222333444",
            "client_id": "507f1f77bcf86cd799439011",
            "count": -1
        }
        coupon = Coupon(**coupon_data)
        assert coupon.count == -1

    def test_coupon_serialization(self):
        """Test coupon model serialization."""
        coupon_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "999888777666"
        }
        coupon = CouponCreate(**coupon_data)
        coupon_dict = coupon.dict()
        assert coupon_dict["company_id"] == "507f1f77bcf86cd799439012"
        assert coupon_dict["barcode"] == "999888777666"

    def test_coupon_json_serialization(self):
        """Test coupon model JSON serialization."""
        coupon_data = {
            "id": "507f1f77bcf86cd799439014",
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "444555666777",
            "client_id": "507f1f77bcf86cd799439011",
            "count": 7
        }
        coupon = Coupon(**coupon_data)
        coupon_json = coupon.json()
        assert '"barcode":"444555666777"' in coupon_json
        assert '"count":7' in coupon_json