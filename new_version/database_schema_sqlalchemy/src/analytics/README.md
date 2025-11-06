# Analytics Schema Setup Guide

Quick setup for the CU Boulder analytics tracking system.

---

## 📋 Prerequisites

- PostgreSQL running with `postgres` database and `asante_dev` user
- Public schema populated (with `app_user` table)
- Python 3.8+ installed

---

## Setup (2 Steps)

### Step 1: Create Analytics Schema & Tables

```bash
cd database_schema_sqlalchemy/migrations/initial_schema/scripts/seed_data
python populate_analytics.py
```

**Creates:**
- `analytics` schema
- `analytics.registration_step` table (6 predefined steps)
- `analytics.registration_interaction` table (main tracking table)
- 7+ indexes for performance

### Step 2: (Optional) Add Test Data

```bash
python analytics_seed_data.py
```

**Generates:**
- 115 test user journeys (69 completed, 46 incomplete)
- 500+ interaction records with realistic timestamps
- Multi-session patterns and backward navigation

---

## Verify in pgAdmin

1. Open `http://localhost:5050` (login: `admin@asante.com` / `AdminPass123!`)
2. Navigate: **Servers** → **Local Development** → **postgres** → **Schemas** → **analytics**
3. Verify tables: `registration_step` (6 rows), `registration_interaction`

**Quick check:**
```sql
SELECT COUNT(*) FROM analytics.registration_step;  -- Should return 6
SELECT COUNT(*) FROM analytics.registration_interaction;  -- 500+ if seed data run
```

---
