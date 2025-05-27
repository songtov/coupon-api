# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based coupon management system for cafes with two user types:
- **Admin users**: Manage companies (cafes), issue coupons, set reward rules, view analytics
- **Client users**: Collect coupons via barcodes, view coupon status, redeem rewards

## Architecture

- **Framework**: FastAPI with async/await patterns
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT-based authentication with role-based access control
- **Package Manager**: uv (intended, not yet configured)
- **Testing**: pytest with pytest-asyncio for async tests

## Project Structure

```
app/
├── main.py          # FastAPI app initialization, startup/shutdown events
├── config.py        # Settings using pydantic-settings, reads from .env
├── db.py           # MongoDB connection management with Motor
├── api/            # API route modules (empty - needs implementation)
├── models/         # Pydantic models for request/response validation
├── schemas/        # MongoDB document schemas
├── core/           # Core functionality (auth, security, etc.)
└── utils/          # Utility functions
```

## Development Commands

Since this project uses uv but doesn't have package files yet, common commands will be:
- `uv run uvicorn app.main:app --reload` - Run development server
- `uv run pytest` - Run tests
- `uv run pytest -v` - Run tests with verbose output

## Key Data Models

Based on the PRD, implement these core models:
- **User**: Admin/client authentication, roles
- **Company**: Cafe/organization managed by admin
- **CouponRule**: Company-specific rules (e.g., 10 coupons = 1 coffee)
- **Coupon**: Barcode-based coupons with company association
- **ClientCoupon**: Client's collected coupons with counts
- **Redemption**: History of reward redemptions

## Authentication Flow

- JWT tokens with role-based permissions
- Admin users can manage their own companies only
- Client users can collect/redeem coupons
- Barcode validation links coupons to companies

## Database Connection

MongoDB connection is handled in `app/db.py` using Motor async driver. The database instance is initialized on FastAPI startup and closed on shutdown.

## Development Status

Project is in initial setup phase. Core FastAPI structure exists but API endpoints, models, and business logic need implementation following the detailed tasks in `tasks/tasks.json`.