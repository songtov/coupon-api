import pytest
from pydantic import ValidationError
from app.models.coupon_rule import CouponRuleBase, CouponRuleCreate, CouponRuleInDB, CouponRule


class TestCouponRuleModels:
    """Test coupon rule Pydantic models."""

    def test_coupon_rule_base_valid(self):
        """Test CouponRuleBase with valid data."""
        rule_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 10,
            "reward": "Free coffee"
        }
        rule = CouponRuleBase(**rule_data)
        assert rule.company_id == "507f1f77bcf86cd799439012"
        assert rule.required_coupons == 10
        assert rule.reward == "Free coffee"

    def test_coupon_rule_base_missing_company_id(self):
        """Test CouponRuleBase with missing company_id."""
        rule_data = {
            "required_coupons": 10,
            "reward": "Free coffee"
        }
        with pytest.raises(ValidationError):
            CouponRuleBase(**rule_data)

    def test_coupon_rule_base_missing_required_coupons(self):
        """Test CouponRuleBase with missing required_coupons."""
        rule_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "reward": "Free coffee"
        }
        with pytest.raises(ValidationError):
            CouponRuleBase(**rule_data)

    def test_coupon_rule_base_missing_reward(self):
        """Test CouponRuleBase with missing reward."""
        rule_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 10
        }
        with pytest.raises(ValidationError):
            CouponRuleBase(**rule_data)

    def test_coupon_rule_base_invalid_required_coupons_type(self):
        """Test CouponRuleBase with invalid required_coupons type."""
        rule_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": "ten",
            "reward": "Free coffee"
        }
        with pytest.raises(ValidationError):
            CouponRuleBase(**rule_data)

    def test_coupon_rule_base_negative_required_coupons(self):
        """Test CouponRuleBase with negative required_coupons."""
        rule_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": -5,
            "reward": "Free coffee"
        }
        rule = CouponRuleBase(**rule_data)
        assert rule.required_coupons == -5

    def test_coupon_rule_base_zero_required_coupons(self):
        """Test CouponRuleBase with zero required_coupons."""
        rule_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 0,
            "reward": "Free coffee"
        }
        rule = CouponRuleBase(**rule_data)
        assert rule.required_coupons == 0

    def test_coupon_rule_create_valid(self):
        """Test CouponRuleCreate with valid data."""
        rule_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 5,
            "reward": "Free pastry"
        }
        rule = CouponRuleCreate(**rule_data)
        assert rule.company_id == "507f1f77bcf86cd799439012"
        assert rule.required_coupons == 5
        assert rule.reward == "Free pastry"

    def test_coupon_rule_in_db_valid(self):
        """Test CouponRuleInDB with valid data."""
        rule_data = {
            "_id": "507f1f77bcf86cd799439013",
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 15,
            "reward": "Free sandwich"
        }
        rule = CouponRuleInDB(**rule_data)
        assert rule.id == "507f1f77bcf86cd799439013"
        assert rule.company_id == "507f1f77bcf86cd799439012"
        assert rule.required_coupons == 15
        assert rule.reward == "Free sandwich"

    def test_coupon_rule_in_db_alias_id(self):
        """Test CouponRuleInDB _id alias works correctly."""
        rule_data = {
            "_id": "507f1f77bcf86cd799439013",
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 8,
            "reward": "Free drink"
        }
        rule = CouponRuleInDB(**rule_data)
        assert rule.id == "507f1f77bcf86cd799439013"

    def test_coupon_rule_in_db_missing_id(self):
        """Test CouponRuleInDB with missing _id."""
        rule_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 8,
            "reward": "Free drink"
        }
        with pytest.raises(ValidationError):
            CouponRuleInDB(**rule_data)

    def test_coupon_rule_valid(self):
        """Test CouponRule model with valid data."""
        rule_data = {
            "id": "507f1f77bcf86cd799439013",
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 12,
            "reward": "Free meal"
        }
        rule = CouponRule(**rule_data)
        assert rule.id == "507f1f77bcf86cd799439013"
        assert rule.company_id == "507f1f77bcf86cd799439012"
        assert rule.required_coupons == 12
        assert rule.reward == "Free meal"

    def test_coupon_rule_missing_id(self):
        """Test CouponRule model without id."""
        rule_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 12,
            "reward": "Free meal"
        }
        with pytest.raises(ValidationError):
            CouponRule(**rule_data)

    def test_coupon_rule_serialization(self):
        """Test coupon rule model serialization."""
        rule_data = {
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 7,
            "reward": "Discount 20%"
        }
        rule = CouponRuleCreate(**rule_data)
        rule_dict = rule.dict()
        assert rule_dict["company_id"] == "507f1f77bcf86cd799439012"
        assert rule_dict["required_coupons"] == 7
        assert rule_dict["reward"] == "Discount 20%"

    def test_coupon_rule_json_serialization(self):
        """Test coupon rule model JSON serialization."""
        rule_data = {
            "id": "507f1f77bcf86cd799439013",
            "company_id": "507f1f77bcf86cd799439012",
            "required_coupons": 6,
            "reward": "Free dessert"
        }
        rule = CouponRule(**rule_data)
        rule_json = rule.json()
        assert '"required_coupons":6' in rule_json
        assert '"reward":"Free dessert"' in rule_json