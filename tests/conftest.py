import pytest
import asyncio
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_db():
    """Create a test MongoDB database."""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.test_coupon_api
    yield db
    # Clean up after tests
    await client.drop_database("test_coupon_api")
    client.close()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "role": "admin",
        "password": "password123"
    }


@pytest.fixture
def sample_company_data():
    """Sample company data for testing."""
    return {
        "name": "Test Cafe",
        "description": "A test cafe for testing",
        "admin_id": "507f1f77bcf86cd799439011"
    }


@pytest.fixture
def sample_coupon_rule_data():
    """Sample coupon rule data for testing."""
    return {
        "company_id": "507f1f77bcf86cd799439012",
        "required_coupons": 10,
        "reward": "Free coffee"
    }


@pytest.fixture
def sample_coupon_data():
    """Sample coupon data for testing."""
    return {
        "company_id": "507f1f77bcf86cd799439012",
        "barcode": "123456789012"
    }