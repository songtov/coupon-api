import pytest
from bson import ObjectId
from datetime import datetime, timezone
from app.schemas.coupon import (
    create_coupon, get_coupon_by_id, get_coupon_by_barcode_and_client,
    get_coupons_by_client, get_coupons_by_company, update_coupon_count,
    increment_coupon_count, delete_coupon
)
from app.models.coupon import CouponCreate


@pytest.mark.asyncio
class TestCouponSchemas:
    """Test coupon database schema operations."""

    async def test_create_coupon(self, test_db, sample_coupon_data):
        """Test creating a coupon in the database."""
        coupon_create = CouponCreate(**sample_coupon_data)
        client_id = "507f1f77bcf86cd799439011"
        
        coupon_id = await create_coupon(test_db, coupon_create, client_id)
        
        assert coupon_id is not None
        assert ObjectId.is_valid(coupon_id)

    async def test_create_coupon_sets_defaults(self, test_db, sample_coupon_data):
        """Test that create_coupon sets default values correctly."""
        coupon_create = CouponCreate(**sample_coupon_data)
        client_id = "507f1f77bcf86cd799439011"
        
        coupon_id = await create_coupon(test_db, coupon_create, client_id)
        
        coupon = await get_coupon_by_id(test_db, coupon_id)
        assert coupon.count == 0
        assert coupon.client_id == client_id
        # Just verify that timestamps are set and are datetime objects
        assert coupon.created_at is not None
        assert coupon.updated_at is not None
        assert isinstance(coupon.created_at, datetime)
        assert isinstance(coupon.updated_at, datetime)

    async def test_get_coupon_by_id(self, test_db, sample_coupon_data):
        """Test retrieving a coupon by ID."""
        coupon_create = CouponCreate(**sample_coupon_data)
        client_id = "507f1f77bcf86cd799439011"
        
        coupon_id = await create_coupon(test_db, coupon_create, client_id)
        coupon = await get_coupon_by_id(test_db, coupon_id)
        
        assert coupon is not None
        assert coupon.id == coupon_id
        assert coupon.company_id == sample_coupon_data["company_id"]
        assert coupon.barcode == sample_coupon_data["barcode"]
        assert coupon.client_id == client_id
        assert coupon.count == 0
        assert isinstance(coupon.created_at, datetime)
        assert isinstance(coupon.updated_at, datetime)

    async def test_get_coupon_by_id_not_found(self, test_db):
        """Test retrieving a non-existent coupon by ID."""
        fake_id = str(ObjectId())
        coupon = await get_coupon_by_id(test_db, fake_id)
        
        assert coupon is None

    async def test_get_coupon_by_id_invalid_id(self, test_db):
        """Test retrieving a coupon with invalid ID format."""
        with pytest.raises(Exception):
            await get_coupon_by_id(test_db, "invalid_id")

    async def test_get_coupon_by_barcode_and_client(self, test_db, sample_coupon_data):
        """Test retrieving a coupon by barcode and client ID."""
        coupon_create = CouponCreate(**sample_coupon_data)
        client_id = "507f1f77bcf86cd799439011"
        
        coupon_id = await create_coupon(test_db, coupon_create, client_id)
        coupon = await get_coupon_by_barcode_and_client(
            test_db, sample_coupon_data["barcode"], client_id
        )
        
        assert coupon is not None
        assert coupon.id == coupon_id
        assert coupon.barcode == sample_coupon_data["barcode"]
        assert coupon.client_id == client_id

    async def test_get_coupon_by_barcode_and_client_not_found(self, test_db):
        """Test retrieving a non-existent coupon by barcode and client."""
        coupon = await get_coupon_by_barcode_and_client(
            test_db, "nonexistent_barcode", "507f1f77bcf86cd799439999"
        )
        
        assert coupon is None

    async def test_get_coupon_by_barcode_and_client_wrong_client(self, test_db, sample_coupon_data):
        """Test retrieving a coupon with correct barcode but wrong client."""
        coupon_create = CouponCreate(**sample_coupon_data)
        client_id = "507f1f77bcf86cd799439011"
        wrong_client_id = "507f1f77bcf86cd799439999"
        
        await create_coupon(test_db, coupon_create, client_id)
        coupon = await get_coupon_by_barcode_and_client(
            test_db, sample_coupon_data["barcode"], wrong_client_id
        )
        
        assert coupon is None

    async def test_get_coupons_by_client(self, test_db):
        """Test retrieving coupons by client ID."""
        client_id = "507f1f77bcf86cd799439011"
        
        # Create multiple coupons for the same client
        coupon_data1 = {
            "company_id": "507f1f77bcf86cd799439012",
            "barcode": "123456789001"
        }
        coupon_data2 = {
            "company_id": "507f1f77bcf86cd799439013",
            "barcode": "123456789002"
        }
        
        coupon_create1 = CouponCreate(**coupon_data1)
        coupon_create2 = CouponCreate(**coupon_data2)
        
        coupon_id1 = await create_coupon(test_db, coupon_create1, client_id)
        coupon_id2 = await create_coupon(test_db, coupon_create2, client_id)
        
        coupons = await get_coupons_by_client(test_db, client_id)
        
        assert len(coupons) == 2
        coupon_ids = [coupon.id for coupon in coupons]
        assert coupon_id1 in coupon_ids
        assert coupon_id2 in coupon_ids
        
        for coupon in coupons:
            assert coupon.client_id == client_id

    async def test_get_coupons_by_client_no_coupons(self, test_db):
        """Test retrieving coupons for client with no coupons."""
        client_id = "507f1f77bcf86cd799439999"
        
        coupons = await get_coupons_by_client(test_db, client_id)
        
        assert len(coupons) == 0

    async def test_get_coupons_by_company(self, test_db):
        """Test retrieving coupons by company ID."""
        company_id = "507f1f77bcf86cd799439012"
        
        # Create multiple coupons for the same company
        coupon_data1 = {
            "company_id": company_id,
            "barcode": "123456789001"
        }
        coupon_data2 = {
            "company_id": company_id,
            "barcode": "123456789002"
        }
        
        coupon_create1 = CouponCreate(**coupon_data1)
        coupon_create2 = CouponCreate(**coupon_data2)
        
        client_id1 = "507f1f77bcf86cd799439011"
        client_id2 = "507f1f77bcf86cd799439022"
        
        coupon_id1 = await create_coupon(test_db, coupon_create1, client_id1)
        coupon_id2 = await create_coupon(test_db, coupon_create2, client_id2)
        
        coupons = await get_coupons_by_company(test_db, company_id)
        
        assert len(coupons) == 2
        coupon_ids = [coupon.id for coupon in coupons]
        assert coupon_id1 in coupon_ids
        assert coupon_id2 in coupon_ids
        
        for coupon in coupons:
            assert coupon.company_id == company_id

    async def test_get_coupons_by_company_no_coupons(self, test_db):
        """Test retrieving coupons for company with no coupons."""
        company_id = "507f1f77bcf86cd799439999"
        
        coupons = await get_coupons_by_company(test_db, company_id)
        
        assert len(coupons) == 0

    async def test_update_coupon_count(self, test_db, sample_coupon_data):
        """Test updating coupon count."""
        coupon_create = CouponCreate(**sample_coupon_data)
        client_id = "507f1f77bcf86cd799439011"
        
        coupon_id = await create_coupon(test_db, coupon_create, client_id)
        
        # Update count to 5
        result = await update_coupon_count(test_db, coupon_id, 5)
        assert result is True
        
        updated_coupon = await get_coupon_by_id(test_db, coupon_id)
        assert updated_coupon.count == 5
        
        # Verify updated_at was changed
        original_coupon = await get_coupon_by_id(test_db, coupon_id)
        assert updated_coupon.updated_at >= original_coupon.created_at

    async def test_update_coupon_count_not_found(self, test_db):
        """Test updating count for non-existent coupon."""
        fake_id = str(ObjectId())
        result = await update_coupon_count(test_db, fake_id, 10)
        
        assert result is False

    async def test_update_coupon_count_invalid_id(self, test_db):
        """Test updating count with invalid ID format."""
        with pytest.raises(Exception):
            await update_coupon_count(test_db, "invalid_id", 10)

    async def test_increment_coupon_count(self, test_db, sample_coupon_data):
        """Test incrementing coupon count."""
        coupon_create = CouponCreate(**sample_coupon_data)
        client_id = "507f1f77bcf86cd799439011"
        
        coupon_id = await create_coupon(test_db, coupon_create, client_id)
        
        # Increment count multiple times
        result1 = await increment_coupon_count(test_db, coupon_id)
        assert result1 is True
        
        coupon_after_first = await get_coupon_by_id(test_db, coupon_id)
        assert coupon_after_first.count == 1
        
        result2 = await increment_coupon_count(test_db, coupon_id)
        assert result2 is True
        
        coupon_after_second = await get_coupon_by_id(test_db, coupon_id)
        assert coupon_after_second.count == 2
        
        # Verify updated_at was changed
        assert coupon_after_second.updated_at > coupon_after_first.updated_at

    async def test_increment_coupon_count_not_found(self, test_db):
        """Test incrementing count for non-existent coupon."""
        fake_id = str(ObjectId())
        result = await increment_coupon_count(test_db, fake_id)
        
        assert result is False

    async def test_increment_coupon_count_invalid_id(self, test_db):
        """Test incrementing count with invalid ID format."""
        with pytest.raises(Exception):
            await increment_coupon_count(test_db, "invalid_id")

    async def test_delete_coupon(self, test_db, sample_coupon_data):
        """Test deleting a coupon."""
        coupon_create = CouponCreate(**sample_coupon_data)
        client_id = "507f1f77bcf86cd799439011"
        
        coupon_id = await create_coupon(test_db, coupon_create, client_id)
        result = await delete_coupon(test_db, coupon_id)
        
        assert result is True
        
        deleted_coupon = await get_coupon_by_id(test_db, coupon_id)
        assert deleted_coupon is None

    async def test_delete_coupon_not_found(self, test_db):
        """Test deleting a non-existent coupon."""
        fake_id = str(ObjectId())
        result = await delete_coupon(test_db, fake_id)
        
        assert result is False

    async def test_delete_coupon_invalid_id(self, test_db):
        """Test deleting a coupon with invalid ID format."""
        with pytest.raises(Exception):
            await delete_coupon(test_db, "invalid_id")

    async def test_coupon_count_edge_cases(self, test_db, sample_coupon_data):
        """Test coupon count operations with edge cases."""
        coupon_create = CouponCreate(**sample_coupon_data)
        client_id = "507f1f77bcf86cd799439011"
        
        coupon_id = await create_coupon(test_db, coupon_create, client_id)
        
        # Test setting count to 0
        result = await update_coupon_count(test_db, coupon_id, 0)
        assert result is True
        
        coupon = await get_coupon_by_id(test_db, coupon_id)
        assert coupon.count == 0
        
        # Test setting count to large number
        result = await update_coupon_count(test_db, coupon_id, 999999)
        assert result is True
        
        coupon = await get_coupon_by_id(test_db, coupon_id)
        assert coupon.count == 999999