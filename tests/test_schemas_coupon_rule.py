import pytest
from bson import ObjectId
from app.schemas.coupon_rule import (
    create_coupon_rule, get_coupon_rule_by_id, get_coupon_rules_by_company,
    update_coupon_rule, delete_coupon_rule
)
from app.models.coupon_rule import CouponRuleCreate


@pytest.mark.asyncio
class TestCouponRuleSchemas:
    """Test coupon rule database schema operations."""

    async def test_create_coupon_rule(self, test_db, sample_coupon_rule_data):
        """Test creating a coupon rule in the database."""
        rule_create = CouponRuleCreate(**sample_coupon_rule_data)
        
        rule_id = await create_coupon_rule(test_db, rule_create)
        
        assert rule_id is not None
        assert ObjectId.is_valid(rule_id)

    async def test_get_coupon_rule_by_id(self, test_db, sample_coupon_rule_data):
        """Test retrieving a coupon rule by ID."""
        rule_create = CouponRuleCreate(**sample_coupon_rule_data)
        
        rule_id = await create_coupon_rule(test_db, rule_create)
        rule = await get_coupon_rule_by_id(test_db, rule_id)
        
        assert rule is not None
        assert rule.id == rule_id
        assert rule.company_id == sample_coupon_rule_data["company_id"]
        assert rule.required_coupons == sample_coupon_rule_data["required_coupons"]
        assert rule.reward == sample_coupon_rule_data["reward"]

    async def test_get_coupon_rule_by_id_not_found(self, test_db):
        """Test retrieving a non-existent coupon rule by ID."""
        fake_id = str(ObjectId())
        rule = await get_coupon_rule_by_id(test_db, fake_id)
        
        assert rule is None

    async def test_get_coupon_rule_by_id_invalid_id(self, test_db):
        """Test retrieving a coupon rule with invalid ID format."""
        with pytest.raises(Exception):
            await get_coupon_rule_by_id(test_db, "invalid_id")

    async def test_get_coupon_rules_by_company(self, test_db):
        """Test retrieving coupon rules by company ID."""
        company_id = "507f1f77bcf86cd799439012"
        
        # Create multiple rules for the same company
        rule_data1 = {
            "company_id": company_id,
            "required_coupons": 5,
            "reward": "Free coffee"
        }
        rule_data2 = {
            "company_id": company_id,
            "required_coupons": 10,
            "reward": "Free pastry"
        }
        
        rule_create1 = CouponRuleCreate(**rule_data1)
        rule_create2 = CouponRuleCreate(**rule_data2)
        
        rule_id1 = await create_coupon_rule(test_db, rule_create1)
        rule_id2 = await create_coupon_rule(test_db, rule_create2)
        
        rules = await get_coupon_rules_by_company(test_db, company_id)
        
        assert len(rules) == 2
        rule_ids = [rule.id for rule in rules]
        assert rule_id1 in rule_ids
        assert rule_id2 in rule_ids
        
        for rule in rules:
            assert rule.company_id == company_id

    async def test_get_coupon_rules_by_company_no_rules(self, test_db):
        """Test retrieving coupon rules for company with no rules."""
        company_id = "507f1f77bcf86cd799439999"
        
        rules = await get_coupon_rules_by_company(test_db, company_id)
        
        assert len(rules) == 0

    async def test_get_coupon_rules_by_company_different_companies(self, test_db):
        """Test that rules are properly filtered by company."""
        company_id1 = "507f1f77bcf86cd799439012"
        company_id2 = "507f1f77bcf86cd799439013"
        
        # Create rules for different companies
        rule_data1 = {
            "company_id": company_id1,
            "required_coupons": 5,
            "reward": "Free coffee"
        }
        rule_data2 = {
            "company_id": company_id2,
            "required_coupons": 8,
            "reward": "Free sandwich"
        }
        
        rule_create1 = CouponRuleCreate(**rule_data1)
        rule_create2 = CouponRuleCreate(**rule_data2)
        
        rule_id1 = await create_coupon_rule(test_db, rule_create1)
        rule_id2 = await create_coupon_rule(test_db, rule_create2)
        
        # Get rules for company 1
        rules1 = await get_coupon_rules_by_company(test_db, company_id1)
        assert len(rules1) == 1
        assert rules1[0].id == rule_id1
        assert rules1[0].company_id == company_id1
        
        # Get rules for company 2
        rules2 = await get_coupon_rules_by_company(test_db, company_id2)
        assert len(rules2) == 1
        assert rules2[0].id == rule_id2
        assert rules2[0].company_id == company_id2

    async def test_update_coupon_rule(self, test_db, sample_coupon_rule_data):
        """Test updating coupon rule data."""
        rule_create = CouponRuleCreate(**sample_coupon_rule_data)
        
        rule_id = await create_coupon_rule(test_db, rule_create)
        
        update_data = {
            "required_coupons": 15,
            "reward": "Free meal"
        }
        result = await update_coupon_rule(test_db, rule_id, update_data)
        
        assert result is True
        
        updated_rule = await get_coupon_rule_by_id(test_db, rule_id)
        assert updated_rule.required_coupons == 15
        assert updated_rule.reward == "Free meal"
        assert updated_rule.company_id == sample_coupon_rule_data["company_id"]

    async def test_update_coupon_rule_not_found(self, test_db):
        """Test updating a non-existent coupon rule."""
        fake_id = str(ObjectId())
        update_data = {"required_coupons": 20}
        
        result = await update_coupon_rule(test_db, fake_id, update_data)
        
        assert result is False

    async def test_update_coupon_rule_invalid_id(self, test_db):
        """Test updating a coupon rule with invalid ID format."""
        update_data = {"required_coupons": 20}
        
        with pytest.raises(Exception):
            await update_coupon_rule(test_db, "invalid_id", update_data)

    async def test_delete_coupon_rule(self, test_db, sample_coupon_rule_data):
        """Test deleting a coupon rule."""
        rule_create = CouponRuleCreate(**sample_coupon_rule_data)
        
        rule_id = await create_coupon_rule(test_db, rule_create)
        result = await delete_coupon_rule(test_db, rule_id)
        
        assert result is True
        
        deleted_rule = await get_coupon_rule_by_id(test_db, rule_id)
        assert deleted_rule is None

    async def test_delete_coupon_rule_not_found(self, test_db):
        """Test deleting a non-existent coupon rule."""
        fake_id = str(ObjectId())
        result = await delete_coupon_rule(test_db, fake_id)
        
        assert result is False

    async def test_delete_coupon_rule_invalid_id(self, test_db):
        """Test deleting a coupon rule with invalid ID format."""
        with pytest.raises(Exception):
            await delete_coupon_rule(test_db, "invalid_id")

    async def test_coupon_rule_edge_cases(self, test_db):
        """Test coupon rule creation with edge case values."""
        # Test with zero required coupons
        rule_data_zero = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 0,
            "reward": "Instant reward"
        }
        rule_create_zero = CouponRuleCreate(**rule_data_zero)
        rule_id_zero = await create_coupon_rule(test_db, rule_create_zero)
        rule_zero = await get_coupon_rule_by_id(test_db, rule_id_zero)
        
        assert rule_zero.required_coupons == 0
        assert rule_zero.reward == "Instant reward"
        
        # Test with high required coupons
        rule_data_high = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 1000,
            "reward": "Mega reward"
        }
        rule_create_high = CouponRuleCreate(**rule_data_high)
        rule_id_high = await create_coupon_rule(test_db, rule_create_high)
        rule_high = await get_coupon_rule_by_id(test_db, rule_id_high)
        
        assert rule_high.required_coupons == 1000
        assert rule_high.reward == "Mega reward"