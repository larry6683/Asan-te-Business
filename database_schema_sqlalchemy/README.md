# Database Layer - SQLAlchemy Models

SQLAlchemy ORM models converted from a raw SQL-based migration system.

## Migration Summary

This database layer was migrated from 100+ SQL files to 6 Python files while maintaining identical functionality.

### What Was Consolidated
- **9 SQL migration files** → **1 Python script** (populate_database.py)
- **12 data population SQL files** → **Functions in populate_database.py**
- **30+ trigger function SQL files** → **3 SQLAlchemy event handlers** (hash generation only)
- **30+ trigger SQL files** → **Automatic SQLAlchemy behavior** (timestamps)
- **13 stored procedure SQL files** → **Python upsert logic**
- **3 seed data SQL files** → **3 Python scripts**
- **All table definition SQL files** → **SQLAlchemy model classes**

### What Stayed
- PostgreSQL-specific SQL files (extensions, schemas, types)
- Helper query files for debugging

## Quick Start

### 1. Setup PostgreSQL Docker Container
See `_dev/README.md` for detailed instructions.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database (One Command)
```bash
# Complete setup (replaces running 9+ SQL files)
python migrations/00_initial_schema/populate_database.py

# Setup without test data
python migrations/00_initial_schema/populate_database.py --no-seed

# Verify existing installation
python migrations/00_initial_schema/populate_database.py --verify-only
```

### 4. Test API Integration
```bash
python test_api_integration.py
```

## Database Management Commands

### Seed Data Management
```bash
# Create test data
python scripts/seed_data/public_seed_data.py

# Remove only test data (surgical)
python scripts/seed_data/delete_seed_data.py

# Clear all business/user data (keep reference data)
python scripts/seed_data/clear_db_data.py

# Nuclear option - completely reset database
python scripts/drop_database_objects.py --confirm
```

### Connection Testing
```bash
python test_postgresql_connection.py
```

## Usage in gRPC API

### Import All Models
```python
from database_layer.src.public.tables import *
```

### Database Connection
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://asante_dev:password@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
```

### Example: User Registration
```python
def create_user(email, user_type_code=1):
    session = Session()
    try:
        user_type = session.query(UserType).filter_by(code=user_type_code).first()
        new_user = AppUser(
            user_type_id=user_type.user_type_id,
            email=email,
            mailing_list_signup=False
        )
        session.add(new_user)
        session.commit()
        return new_user
    finally:
        session.close()
```

### Example: Business Registration
```python
def create_business(business_name, email, city, state, size_code=2):
    session = Session()
    try:
        business_size = session.query(BusinessSize).filter_by(code=size_code).first()
        new_business = Business(
            business_name=business_name,
            email=email,
            location_city=city,
            location_state=state,
            business_size_id=business_size.business_size_id
        )
        session.add(new_business)
        session.commit()
        return new_business
    finally:
        session.close()
```

## Models Available

**User Tables:**
- `UserType`, `AppUser`, `RegistrationType`

**System/Reference Tables:**
- `CauseCategory`, `Cause`, `CausePreferenceRank`
- `SocialMediaType`, `ShopType`

**Business Tables:**
- `BusinessSize`, `BusinessUserPermissionRole`, `Business`
- `BusinessUser`, `BusinessCausePreference`, `BusinessSocialMedia`
- `BusinessShop`, `BusinessImpactLink`

**Beneficiary Tables:**
- `BeneficiarySize`, `BeneficiaryUserPermissionRole`
- `Beneficiary`, `BeneficiaryUser`, `BeneficiaryCausePreference`
- `BeneficiarySocialMedia`, `BeneficiaryShop`

## Test Data Created

The setup creates three test businesses with complete data:

- **Eco Solutions Inc.** (Seattle, WA) - Medium size, Environmental causes
- **Tech Innovations Ltd** (San Francisco, CA) - Large size, Education causes  
- **Local Harvest Co-op** (Portland, OR) - Small size, Community causes

Each business includes:
- 4 test users (2 admins, 2 team members)
- Social media profiles
- Cause preferences
- Shop integrations
- Impact links

## Migration Benefits

**Before:** Manual process requiring correct execution order of 9+ SQL files
**After:** Single command setup with automatic dependency resolution

**Before:** Separate SQL files for each operation (populate, clear, delete data)
**After:** Individual Python scripts with better error handling

**Before:** SQL triggers and functions for hash generation and timestamps
**After:** SQLAlchemy events and automatic timestamp updates

**Before:** SQL stored procedures for upsert operations
**After:** Python upsert logic with better maintainability

## Technical Notes

- All models include `created_at` and `updated_at` timestamps
- UUIDs are used for all primary keys
- Foreign key relationships are properly defined
- Hash fields (`email_hash`, `business_name_hash`) auto-generated via SQLAlchemy events
- Original SQL functionality preserved but implemented more efficiently

## Project Structure

```
database_layer/
├── migrations/00_initial_schema/
│   ├── 01_create_extensions.sql     # PostgreSQL extensions
│   ├── 02_create_schemas.sql        # Schema creation
│   ├── 03_create_types.sql          # Custom types
│   └── populate_database.py         # Main setup script
├── scripts/
│   ├── seed_data/                   # Data management scripts
│   └── drop_database_objects.py     # Nuclear reset option
└── src/public/tables/               # SQLAlchemy model definitions
```

## Troubleshooting

**Connection Issues:** Ensure Docker PostgreSQL is running on localhost:5432
**Credentials:** asante_dev / password / postgres database
**Import Errors:** Run from project root directory where database_layer/ exists
**Duplicate Data:** Use `--no-seed` flag or clear existing data first

**Migration Questions:** See `src/public/tables/README.md` for detailed migration mapping

## Database Connection Details

- **Host:** localhost
- **Port:** 5432
- **Database:** postgres
- **Username:** asante_dev
- **Password:** password