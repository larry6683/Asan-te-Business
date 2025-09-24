# Database Schema - SQLAlchemy Models

SQLAlchemy ORM models converted from raw SQL definitions.

## Quick Start

### 1. Setup PostgreSQL Docker Container

See database-schema/_dev/README.md for detailed instructions.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Database
```bash
python database_layer/setup_database.py
```

### 4. Test API Integration
```bash
python test_api_integration.py
```

## Usage in gRPC API

### Import All Models
```python
from database_layer.models import *
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

## Additional Commands

```bash
# Setup without test data
python database_layer/setup_database.py --no-seed

# Verify existing data
python database_layer/setup_database.py --verify-only

# Test connection (alternative, see doc string in file for more info)
python database_layer/test_postgresql_connection.py
```

## Test Data Created

- **Eco Solutions Inc.** (Seattle, WA) - Environmental causes
- **Tech Innovations Ltd** (San Francisco, CA) - Education causes  
- **Local Harvest Co-op** (Portland, OR) - Community causes

Each business includes users, social media, cause preferences, and shops.

## Troubleshooting

**Connection Issues:** Ensure Docker PostgreSQL is running on localhost:5432
**Credentials:** asante_dev / password / postgres database
**Import Errors:** Run from project root directory where database_layer/ exists


## Commands

### Setup Database from Scratch
```bash
python database_layer/setup_database.py
```

### Setup Without Test Data
```bash
python database_layer/setup_database.py --no-seed
```

### Verify Existing Data
```bash
python database_layer/setup_database.py --verify-only
```

### Test PostgreSQL Connection (Alternative)
```bash
python database_layer/test_postgresql_connection.py
```

## Test Data

The setup creates test businesses:
- **Eco Solutions Inc.** (Seattle, WA) - Medium size, Environmental causes
- **Tech Innovations Ltd** (San Francisco, CA) - Large size, Education causes  
- **Local Harvest Co-op** (Portland, OR) - Small size, Community causes

Each business has 4 test users (2 admins, 2 team members).

## Models Available

**User Tables:**
- `UserType`, `AppUser`, `RegistrationType`, `AppUserRegistrationType`

**Domain/System Type Data:**
- `CauseCategory`, `Cause`, `CausePreferenceRank`, `SocialMediaType`, `ShopType`

**Business Tables:**
- `BusinessSize`, `BusinessUserPermissionRole`, `BusinessType`, `Business`
- `BusinessUser`, `BusinessCausePreference`, `BusinessSocialMedia`
- `BusinessShop`, `BusinessImpactLink`

**Beneficiary Tables:**
- `BeneficiarySize`, `BeneficiaryUserPermissionRole`, `BeneficiaryType`
- `Beneficiary`, `BeneficiaryUser`, `BeneficiaryCausePreference`
- `BeneficiarySocialMedia`, `BeneficiaryShop`

## Notes

- All models include `created_at` and `updated_at` timestamps
- UUIDs are used for all primary keys
- Foreign key relationships are properly defined
- Hash fields (`email_hash`, `business_name_hash`) are included but not auto-populated
- Original SQL triggers converted to SQLAlchemy `onupdate` functionality

## Troubleshooting

### Duplicate Data Errors
If you get unique constraint violations, clear existing data first or use `--no-seed` flag.