# 🔧 gRPC API Services

Clean implementation of gRPC microservices for User, Business, Beneficiary, and Analytics management.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Services](#-services)
- [Project Structure](#-project-structure)
- [Setup](#-setup)
- [Running Services](#-running-services)
- [Testing](#-testing)
- [Development](#-development)

---

## 🎯 Overview

This backend implements a **CQRS Vertical Slices** pattern with four independent gRPC microservices:
- Separation of Command and Query handlers
- SQLAlchemy ORM for database operations
- Protocol Buffers for service definitions
- Docker support for containerization

**Architecture Pattern**: Each service is independently deployable with its own:
- Command handlers (create, update operations)
- Query handlers (read operations)
- Domain models and converters
- Database connection management

---

## 🚀 Services

### User Service (Port 50051)
Handles user authentication and profile management.

**RPC Methods:**
- `GetUser(email)` → User
- `CreateUser(email, user_type, mailing_list_signup)` → User
- `GetUserByEmail(email)` → User

**Features:**
- Cognito integration
- Session management
- User type classification (business/beneficiary)

### Business Service (Port 50052)
Manages business registration and profiles.

**RPC Methods:**
- `GetBusiness(business_id)` → Business
- `CreateBusiness(...)` → Business
- `GetBusinessByUser(user_id)` → Business
- `UpdateBusiness(...)` → Business

**Features:**
- Cause selection (multiple causes)
- Size classification
- Business entity information
- Tax ID management

### Beneficiary Service (Port 50053)
Handles non-profit organization registration.

**RPC Methods:**
- `GetBeneficiary(beneficiary_id)` → Beneficiary
- `CreateBeneficiary(...)` → Beneficiary
- `GetBeneficiaryByUser(user_id)` → Beneficiary
- `UpdateBeneficiary(...)` → Beneficiary

**Features:**
- Primary and supporting causes
- Organization size classification
- EIN management
- Mission statement handling

### Analytics Service (Port 50054)
Tracks user journeys and provides dashboard metrics.

**RPC Methods:**
- `GetDashboardKPIs()` → KPIs
- `TrackRegistrationInteraction(...)` → Success
- `GetRegistrationFunnel()` → FunnelData

**Features:**
- Real-time KPI calculation
- Session tracking
- Registration completion rates
- User journey analytics

---

## 📂 Project Structure

```
new-grpc-api/
├── src/
│   ├── protos/                      # Protocol Buffer definitions
│   │   ├── user/user.proto
│   │   ├── business/business.proto
│   │   ├── beneficiary/beneficiary.proto
│   │   ├── analytics/analytics.proto
│   │   └── error/error.proto
│   │
│   ├── codegen/                     # Generated gRPC code (auto-generated)
│   │   ├── user/
│   │   ├── business/
│   │   ├── beneficiary/
│   │   ├── analytics/
│   │   └── error/
│   │
│   ├── services/                    # Service implementations
│   │   ├── user/
│   │   │   ├── server.py           # gRPC server
│   │   │   ├── handlers/           # Request handlers
│   │   │   └── queries/            # Query logic
│   │   ├── business/
│   │   ├── beneficiary/
│   │   └── analytics/
│   │
│   ├── domain/                      # Domain models (DTOs)
│   │   ├── user.py
│   │   ├── business.py
│   │   ├── beneficiary.py
│   │   └── analytics.py
│   │
│   ├── converters/                  # Database to domain converters
│   │   ├── user_converter.py
│   │   ├── business_converter.py
│   │   └── beneficiary_converter.py
│   │
│   ├── database/                    # Database connection
│   │   └── connection.py
│   │
│   ├── config/                      # Configuration
│   │   └── config.py
│   │
│   └── utils/                       # Utilities
│       ├── cause_mapping.py
│       └── enum_converters.py
│
├── scripts/
│   └── generate-proto.sh            # Proto generation script
│
├── .env                             # Environment config (not in git)
├── .env.example                     # Environment template
├── requirements.txt                 # Python dependencies
├── run_user_service.sh              # User service runner
├── run_business_service.sh          # Business service runner
├── run_beneficiary_service.sh       # Beneficiary service runner
├── run_analytics_service.sh         # Analytics service runner
├── run_all_services.sh              # Run all services
├── test_services.py                 # Test script
└── README.md                        # This file
```

---

## 🛠️ Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- PostgreSQL database running (see main README)
- Protocol buffer compiler (`protoc`)

### 1. Install Dependencies

```bash
cd new-grpc-api
pip install -r requirements.txt
```

**Required packages:**
```
grpcio>=1.50.0
grpcio-tools>=1.50.0
protobuf>=4.21.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
python-dotenv>=0.19.0
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

**Required environment variables:**
```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=asante_dev
DB_PASSWORD=your_password

# Service Ports
USER_SERVICE_PORT=50051
BUSINESS_SERVICE_PORT=50052
BENEFICIARY_SERVICE_PORT=50053
ANALYTICS_SERVICE_PORT=50054
```

### 3. Ensure Database is Running

```bash
cd ../database_schema_sqlalchemy/_dev
bash setup-postgres-dev.sh

# Verify tables exist
docker exec -it asante-postgres-dev psql -U asante_dev -d postgres -c "\dt"
```

### 4. Generate Protobuf Code

**IMPORTANT:** This must be done before starting services!

```bash
cd new-grpc-api
./scripts/generate-proto.sh
```

This will:
- Generate Python code from `.proto` files
- Fix import paths automatically
- Create necessary `__init__.py` files

---

## ▶️ Running Services

### Option 1: Run All Services (Recommended)

```bash
cd new-grpc-api
./run_all_services.sh
```

This starts all four services in the background and shows their logs.

**To stop:**
```bash
# Find PIDs
ps aux | grep "python src/services"

# Kill all
pkill -f "python src/services"
```

### Option 2: Run Services Individually

Open **4 separate terminals**:

**Terminal 1 - User Service:**
```bash
cd new-grpc-api
./run_user_service.sh
```

**Terminal 2 - Business Service:**
```bash
cd new-grpc-api
./run_business_service.sh
```

**Terminal 3 - Beneficiary Service:**
```bash
cd new-grpc-api
./run_beneficiary_service.sh
```

**Terminal 4 - Analytics Service:**
```bash
cd new-grpc-api
./run_analytics_service.sh
```

### Verify Services are Running

```bash
# Check if services are listening on ports
lsof -i :50051  # User Service
lsof -i :50052  # Business Service
lsof -i :50053  # Beneficiary Service
lsof -i :50054  # Analytics Service
```

**Expected output:**
```
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python  12345 user    6u  IPv6  ...      0t0  TCP *:50051 (LISTEN)
```

---

## 🧪 Testing

### Using grpcurl

Install grpcurl:
```bash
# macOS
brew install grpcurl

# Linux
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest
```

**List available services:**
```bash
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50052 list
grpcurl -plaintext localhost:50053 list
grpcurl -plaintext localhost:50054 list
```

**Test User Service:**
```bash
# Create user
grpcurl -plaintext -d '{
  "email": "test@example.com",
  "user_type": "BUSINESS",
  "mailing_list_signup": true
}' localhost:50051 user.UserService/CreateUser

# Get user
grpcurl -plaintext -d '{
  "email": "test@example.com"
}' localhost:50051 user.UserService/GetUser
```

**Test Analytics Service:**
```bash
# Get dashboard KPIs
grpcurl -plaintext -d '{}' localhost:50054 analytics.AnalyticsService/GetDashboardKPIs
```

### Using Python Test Script

```bash
python test_services.py
```

### Using Postman

1. Import gRPC service definitions
2. Set endpoint to `localhost:5005X` (X = 1,2,3,4)
3. Select method from proto definition
4. Send request with JSON payload

---

## 🔧 Development

### Project Guidelines

1. **CQRS Pattern**: Separate command and query handlers
2. **Error Handling**: Use structured error responses
3. **Logging**: Include debug logging for troubleshooting
4. **Type Safety**: Use domain models, not raw dictionaries
5. **Database**: Always use SQLAlchemy ORM, never raw SQL

### Adding a New Service

1. **Create proto definition** in `src/protos/`
2. **Generate code**: Run `./scripts/generate-proto.sh`
3. **Create service directory** in `src/services/`
4. **Implement handlers** following CQRS pattern
5. **Add domain models** in `src/domain/`
6. **Create converters** in `src/converters/`
7. **Update Envoy config** to route to new service
8. **Create runner script** like `run_new_service.sh`

### Code Style

- Follow PEP 8 conventions
- Use type hints where possible
- Document all public methods
- Keep handlers focused and single-purpose
- Use meaningful variable names

### Debugging

**Enable debug logging:**
```python
# In service file
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check database connection:**
```bash
python test_db_connection.py
```

**Common Issues:**

| Issue | Solution |
|-------|----------|
| Import errors | Regenerate proto files |
| 503 errors | Check if service is running on correct port |
| Database errors | Verify database is running and credentials are correct |
| Proto not found | Ensure `src/protos/` contains all `.proto` files |

---

## 📝 Additional Resources

- [gRPC Python Quickstart](https://grpc.io/docs/languages/python/quickstart/)
- [Protocol Buffers Guide](https://developers.google.com/protocol-buffers/docs/pythontutorial)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)

---

## 🤝 Contributing

When contributing to backend services:

1. Follow the established CQRS pattern
2. Add tests for new handlers
3. Update proto definitions as needed
4. Document all new RPC methods
5. Ensure backward compatibility

---
