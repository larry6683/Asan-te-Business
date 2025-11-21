# 🗄️ Database Layer - SQLAlchemy ORM

Modern database layer for ASANTe Platform using SQLAlchemy ORM with PostgreSQL.

---

## 🎯 Overview

This database layer consolidates 100+ SQL files into a clean Python implementation while maintaining identical functionality.

**Migration Summary:**

| Component | Before | After |
|-----------|--------|-------|
| Migration files | 9 SQL files | 1 Python script |
| Data population | 12 SQL files | Python functions |
| Triggers | 30+ SQL files | 3 SQLAlchemy events |
| Stored procedures | 13 SQL files | Python logic |
| Seed data | 3 SQL files | 3 Python scripts |

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Python 3.8+ with pip
- Git

### 1. Setup PostgreSQL Database

```bash
cd database_schema_sqlalchemy/_dev

# Start PostgreSQL and pgAdmin containers
bash setup-postgres-dev.sh

# Wait for containers to initialize (30 seconds)
sleep 30
```

**Services:**
- PostgreSQL: `http://localhost:5432`
- pgAdmin: `http://localhost:5050`

**Credentials:** See `.env` file in `_dev/` directory

### 2. Configure pgAdmin (First Time Only)

1. Open `http://localhost:5050`
2. Login with credentials from `.env` (`PGADMIN_DEFAULT_EMAIL` / `PGADMIN_DEFAULT_PASSWORD`)
3. Right-click "Servers" → "Register" → "Server"
4. **General tab:** Name = `Local Development`
5. **Connection tab:**
   - Host: `postgres` (not localhost!)
   - Port: `5432`
   - Database: Value of `DB_NAME` from `.env`
   - Username: Value of `DB_USER` from `.env`
   - Password: Value of `DB_PASSWORD` from `.env`
   - ✅ Save password
6. Click "Save"

### 3. Initialize Database

```bash
cd migrations/initial_schema

# Complete setup (schema + test data)
python populate_data.py

# Or without test data
python populate_data.py --no-seed
```

**This creates:**
- 26+ database tables (public schema)
- Analytics schema with tracking tables
- Reference data (causes, sizes, types)
- 6 registration steps
- Optional: 3 test businesses with users

### 4. Verify Setup

```bash
# Check tables exist
docker exec -it asante-postgres-dev psql -U asante_dev -d postgres -c "\dt"

# Should show 26+ tables
```

---

## 📊 Database Schema

### Public Schema Tables

**Users & Authentication**
- `app_user` - User accounts
- `user_type` - Business / Non-Profit types
- `registration_type` - Registration type tracking

**Reference Data**
- `cause_category` - 26 cause categories
- `cause` - Individual causes within categories
- `social_media_type` - Social platform types
- `shop_type` - E-commerce platform types

**Business**
- `business` - Business entities
- `business_size` - Size classifications
- `business_user` - User-business relationships
- `business_cause_preference` - Selected causes
- `business_social_media` - Social profiles
- `business_shop` - Shop integrations
- `business_impact_link` - Impact documentation

**Beneficiary (Non-Profit)**
- `beneficiary` - Non-profit entities
- `beneficiary_size` - Size classifications
- `beneficiary_user` - User-beneficiary relationships
- `beneficiary_cause_preference` - Selected causes
- `beneficiary_social_media` - Social profiles
- `beneficiary_shop` - Shop integrations

### Analytics Schema Tables

**Registration Tracking**
- `registration_step` - 6 predefined steps:
  1. `signup` - Account creation
  2. `verification` - Email verification
  3. `first_login` - First login after verification
  4. `cause_selection` - Cause preferences
  5. `size` - Organization size
  6. `entity_information` - Final details

- `registration_interaction` - User journey tracking
  - Session-based tracking
  - Step navigation history
  - Timestamps for analytics
  - Multi-session support

- `verification_tracking` - Email verification
  - Verification status
  - Code request counts
  - Attempt timestamps

**Performance Features:**
- 7+ optimized indexes
- Partial indexes for incomplete steps
- Session-based query optimization
- Dropout analysis support

---

## 💻 Usage in Code

### Import Models

```python
# Public schema models
from database_schema_sqlalchemy.src.public.tables import (
    AppUser, UserType, Business, Beneficiary,
    Cause, CauseCategory
)

# Analytics schema models
from database_schema_sqlalchemy.src.analytics.tables import (
    RegistrationStep, RegistrationInteraction, VerificationTracking
)
```

### Database Connection

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Load from environment variables
database_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
```

### Example: Create User

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

### Example: Track Registration Step

```python
from sqlalchemy import func
import uuid

def track_step(session_id, step_name, app_user_id=None):
    session = Session()
    try:
        # Get registration step
        step = session.query(RegistrationStep).filter_by(step_name=step_name).first()
        
        # Create interaction
        interaction = RegistrationInteraction(
            session_id=session_id,
            registration_step_id=step.registration_step_id,
            app_user_id=app_user_id,
            step_began_at=func.now()
        )
        session.add(interaction)
        session.commit()
        return interaction
    finally:
        session.close()
```

### Example: Get Dashboard KPIs

```python
from sqlalchemy import func

def get_dashboard_kpis():
    session = Session()
    try:
        kpis = {
            'total_users': session.query(func.count(AppUser.app_user_id)).scalar(),
            'total_businesses': session.query(func.count(Business.business_id)).scalar(),
            'total_beneficiaries': session.query(func.count(Beneficiary.beneficiary_id)).scalar(),
            'total_sessions': session.query(
                func.count(func.distinct(RegistrationInteraction.session_id))
            ).scalar()
        }
        return kpis
    finally:
        session.close()
```

---

## 🛠️ Data Management

### Test Data

**Create test data:**
```bash
cd _dev
bash create_seed_data.sh
```

**Test data includes:**
- **Eco Solutions Inc.** (Seattle, WA) - Environmental causes
- **Tech Innovations Ltd** (San Francisco, CA) - Education causes
- **Local Harvest Co-op** (Portland, OR) - Community causes
- 4 users per business (2 admins, 2 members)
- Social media profiles, cause preferences, shops

**Reset test data:**
```bash
cd _dev
bash reset_seed_data.sh
```

**Clear all business/user data (keep reference data):**
```bash
cd scripts/seed_data
python clear_db_data.py
```

**Nuclear reset (complete wipe):**
```bash
cd scripts
python drop_database_objects.py --confirm
```

### Analytics Test Data

```bash
cd scripts/seed_data
python analytics_seed_data.py
```

**Generates:**
- 115 user journeys (69 completed, 46 incomplete)
- 500+ interaction records
- Realistic timestamps and navigation patterns

---

## 📊 Analytics Queries

### Completion Rate by Step

```sql
SELECT 
    rs.step_name,
    COUNT(DISTINCT ri.session_id) as sessions_reached,
    COUNT(DISTINCT CASE WHEN ri.step_completed_at IS NOT NULL 
        THEN ri.session_id END) as sessions_completed,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN ri.step_completed_at IS NOT NULL 
        THEN ri.session_id END) / COUNT(DISTINCT ri.session_id), 2) as completion_rate
FROM analytics.registration_step rs
LEFT JOIN analytics.registration_interaction ri 
    ON rs.registration_step_id = ri.registration_step_id
GROUP BY rs.step_name, rs.step_order
ORDER BY rs.step_order;
```

### Average Time per Step

```sql
SELECT 
    rs.step_name,
    AVG(EXTRACT(EPOCH FROM (ri.step_completed_at - ri.step_began_at))) as avg_seconds
FROM analytics.registration_step rs
JOIN analytics.registration_interaction ri 
    ON rs.registration_step_id = ri.registration_step_id
WHERE ri.step_completed_at IS NOT NULL
GROUP BY rs.step_name, rs.step_order
ORDER BY rs.step_order;
```

### User Journey

```sql
SELECT 
    rs.step_name,
    ri.step_began_at,
    ri.step_completed_at,
    EXTRACT(EPOCH FROM (ri.step_completed_at - ri.step_began_at)) as duration_seconds
FROM analytics.registration_interaction ri
JOIN analytics.registration_step rs 
    ON ri.registration_step_id = rs.registration_step_id
WHERE ri.session_id = 'your-session-uuid'
ORDER BY ri.step_began_at;
```

---

## ⚙️ Configuration

Database credentials are managed via `.env` file in `_dev/` directory.

**Create your .env file:**
```bash
cd _dev
cp template.env .env
nano .env  # Edit with your credentials
```

**Required variables:**
```env
# PostgreSQL Configuration
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=localhost(your hostname)
PORT =5432

# pgAdmin Configuration
PGADMIN_DEFAULT_EMAIL=admin_email_
PGADMIN_DEFAULT_PASSWORD=your_admin_password
```

> ⚠️ **Security:** Never commit `.env` to version control. It's in `.gitignore`.

---

## 📂 Project Structure

```
database_schema_sqlalchemy/
├── _dev/                           # Development environment
│   ├── .env                        # Credentials (not in git)
│   ├── template.env                # Template for new users
│   ├── compose.yaml                # Docker Compose config
│   ├── setup-postgres-dev.sh       # Setup script
│   ├── create_seed_data.sh         # Create test data
│   └── reset_seed_data.sh          # Reset test data
│
├── migrations/
│   └── initial_schema/
│       └── populate_data.py        # Main setup script
│
├── scripts/
│   ├── seed_data/
│   │   ├── public_seed_data.py     # Business test data
│   │   ├── analytics_seed_data.py  # Analytics test data
│   │   └── clear_db_data.py        # Clear data
│   └── drop_database_objects.py    # Nuclear reset
│
├── src/
│   ├── public/
│   │   └── tables/                 # Public schema models
│   │       ├── user.py
│   │       ├── business.py
│   │       ├── beneficiary.py
│   │       ├── cause.py
│   │       └── ...
│   └── analytics/
│       ├── tables/                 # Analytics schema models
│       │   ├── registration_step.py
│       │   ├── registration_interaction.py
│       │   └── verification_tracking.py
│       └── README.md               # Analytics docs
│
└── requirements.txt                # Python dependencies
```

---

## 🔧 Troubleshooting

### Database Won't Start

```bash
cd _dev
docker-compose down
docker-compose up -d
sleep 30
```

### Connection Errors

```bash
# Verify containers are running
docker ps | grep asante

# Check logs
docker logs asante-postgres-dev
docker logs asante-pgadmin

# Test connection
docker exec -it asante-postgres-dev psql -U asante_dev -d postgres
```

### Import Errors

```bash
# Ensure running from project root
cd database_schema_sqlalchemy

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt
```

### No Tables Found

```bash
# Repopulate database
cd migrations/initial_schema
python populate_data.py

# Verify
docker exec -it asante-postgres-dev psql -U asante_dev -d postgres -c "\dt"
```

### Permission Issues

```bash
# Grant privileges (run in psql)
GRANT ALL PRIVILEGES ON DATABASE postgres TO asante_dev;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO asante_dev;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO asante_dev;
```

---

## 🧪 Testing

### Connection Test

```bash
cd migrations/initial_schema
python populate_data.py --verify-only
```

### Query Test

```bash
docker exec -it asante-postgres-dev psql -U asante_dev -d postgres

# Test queries
SELECT COUNT(*) FROM app_user;
SELECT COUNT(*) FROM business;
SELECT COUNT(*) FROM analytics.registration_step;

\q
```

### Backend Integration Test

```bash
cd ../../new-grpc-api
python test_db_connection.py
```

---

## ✨ Features

- ✅ **Automatic Timestamps** - `created_at` and `updated_at` on all tables
- ✅ **UUID Primary Keys** - Globally unique identifiers
- ✅ **Auto-generated Hashes** - Email and name hashes for indexing
- ✅ **Foreign Key Relationships** - Proper referential integrity
- ✅ **SQLAlchemy Events** - Replace SQL triggers
- ✅ **Type-Safe Models** - Python type hints throughout
- ✅ **Analytics Tracking** - Multi-session registration journeys
- ✅ **Performance Indexes** - Optimized for common queries
- ✅ **Verification Monitoring** - Track email verification attempts

---

## 📚 Additional Resources

- **Development Setup:** `_dev/README.md`
- **Analytics Details:** `src/analytics/README.md`
- **Model Details:** `src/public/tables/README.md`
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **PostgreSQL Docs:** https://www.postgresql.org/docs/

---

## 🤝 Contributing

When modifying the database layer:

1. **Update models** in `src/public/tables/` or `src/analytics/tables/`
2. **Test locally** with Docker PostgreSQL
3. **Update migration scripts** if needed
4. **Document changes** in this README
5. **Test with backend services** before committing

---
