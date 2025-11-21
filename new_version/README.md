<div align="center">

# 🌟 ASANTe Platform

### Business Registration & Analytics Platform

[![React](https://img.shields.io/badge/React-18.x-61DAFB?style=flat&logo=react&logoColor=white)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![gRPC](https://img.shields.io/badge/gRPC-Web-4285F4?style=flat&logo=google&logoColor=white)](https://grpc.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![AWS Cognito](https://img.shields.io/badge/AWS-Cognito-FF9900?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/cognito/)

*A comprehensive platform connecting businesses with non-profit beneficiaries through a seamless registration flow and powerful analytics.*

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🎯 Overview

ASANTe is a full-stack platform that enables:
- **Businesses** to register and connect with social causes
- **Non-profits** (beneficiaries) to create profiles and receive support
- **Analytics** tracking for user journeys and engagement metrics
- **Multi-step registration** with cause mapping across 26 categories

Built with modern microservices architecture, featuring React frontend, Python gRPC backend, and PostgreSQL database.

---

## ✨ Features

### 🔐 Authentication & User Management
- AWS Cognito integration for secure authentication
- Email verification with code-based confirmation
- Session management with secure cookies
- Automatic redirect handling for incomplete registrations

### 📝 Registration Flow
- **6-Step Process**: Signup → Verification → First Login → Causes → Size → Entity Info
- **Business Registration**: Cause selection, size classification, detailed information
- **Beneficiary Registration**: Primary/supporting causes, organization details
- **Form Validation**: Real-time error handling and user feedback

### 📊 Analytics Dashboard
- Real-time KPI tracking (users, sessions, businesses, beneficiaries)
- Session interaction monitoring
- Registration completion funnel analysis
- Responsive design for mobile, tablet, and desktop

### 🎨 User Experience
- Modern glassmorphism UI with gradient backgrounds
- Fully responsive layouts across all device sizes
- Smooth animations and transitions
- Accessibility-focused design

---

## 📦 Prerequisites

Ensure you have the following installed:

| Tool | Version | Purpose |
|------|---------|---------|
| **Docker Desktop** | Latest | Container orchestration |
| **Node.js** | 16+ | Frontend development |
| **Python** | 3.8+ | Backend services |
| **npm/yarn** | Latest | Package management |
| **Git** | Latest | Version control |

---

## 🚀 Quick Start

### 1️⃣ Clone & Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd asante-platform

# Install frontend dependencies
cd registration-flow-client
npm install
cd ..

# Install backend dependencies
cd new-grpc-api
pip install -r requirements.txt
cd ..
```

### 2️⃣ Configure Environment Variables

Create environment configuration files from templates:

```bash
# Frontend configuration
cd registration-flow-client
cp .env.example .env.local
# Edit .env.local with your AWS Cognito credentials
cd ..

# Backend configuration
cd new-grpc-api
cp .env.example .env
# Edit .env with your database credentials
cd ..

# Database configuration
cd database_schema_sqlalchemy/_dev
cp template.env .env
# Edit .env with your PostgreSQL settings
cd ../..
```

> 📝 **Note**: See [Configuration](#-configuration) section for detailed setup instructions.

### 3️⃣ Set Up Docker Network

```bash
docker network create asante-network
```

### 4️⃣ Start PostgreSQL Database

```bash
cd database_schema_sqlalchemy/
cd _dev

# Start database containers
bash setup-postgres-dev.sh

# Wait for containers to initialize
sleep 30

# Populate database schema and initial data
cd ../migrations/initial_schema
python populate_public_schema.py
python populate_analytics_schema.py
```

**Verify database setup:**
```bash
docker exec -it asante-postgres-dev psql -U asante_dev -d postgres -c "\dt"
```

You should see 26 tables listed.

### 5️⃣ Start Envoy Proxy

```bash
cd envoy_proxy

# Using Docker Compose (recommended)
docker-compose up -d

```

**Verify Envoy is running:**
```bash
curl http://localhost:9901/ready
# Should return: LIVE
```

### 6️⃣ Generate Protobuf Files

**Backend (Python):**
```bash
cd new-grpc-api
./scripts/generate-proto.sh
```

**Frontend (JavaScript):**
```bash
cd registration-flow-client
./scripts/generate-proto.sh
```

### 7️⃣ Start Backend Services

Open 4 separate terminals for each service:

```bash
# Terminal 1: User Service (port 50051)
cd new-grpc-api
./run_user_service.sh

# Terminal 2: Business Service (port 50052)
cd new-grpc-api
./run_business_service.sh

# Terminal 3: Beneficiary Service (port 50053)
cd new-grpc-api
./run_beneficiary_service.sh

# Terminal 4: Analytics Service (port 50054)
cd new-grpc-api
./run_analytics_service.sh
```

**Alternative - Start all services at once:**
```bash
cd new-grpc-api
./run_all_services.sh
```

### 8️⃣ Start Frontend Application

```bash
cd registration-flow-client
npm start
```

**Application will open at:** `http://localhost:3000`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 3000)                │
│              Material-UI • gRPC-Web • AWS Cognito            │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/1.1 (gRPC-Web)
┌────────────────────────────▼────────────────────────────────┐
│                    Envoy Proxy (Port 8080)                   │
│              gRPC-Web ↔ gRPC Transcoding • CORS              │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/2 (native gRPC)
┌────────────────────────────▼────────────────────────────────┐
│                    Python gRPC Services                      │
├──────────────────────────────────────────────────────────────┤
│  • User Service (50051)        • Analytics Service (50054)  │
│  • Business Service (50052)    • CQRS Pattern               │
│  • Beneficiary Service (50053) • SQLAlchemy ORM             │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│              PostgreSQL Database (Port 5432)                 │
│              26 Tables • 26 Cause Categories                 │
│              pgAdmin Web UI (Port 5050)                      │
└──────────────────────────────────────────────────────────────┘
```

### Microservices Architecture

- **User Service**: Authentication, user management, session handling
- **Business Service**: Business registration, cause mapping, profile management
- **Beneficiary Service**: Non-profit registration, cause selection, entity details
- **Analytics Service**: KPI tracking, session monitoring, funnel analysis

### Technology Stack

**Frontend:**
- React 18 with hooks
- Material-UI components
- gRPC-Web for API communication
- AWS Cognito SDK for authentication
- Cookie-based session management

**Backend:**
- Python 3.8+ with asyncio
- gRPC & Protocol Buffers
- SQLAlchemy ORM
- PostgreSQL 14+
- CQRS vertical slices pattern

**Infrastructure:**
- Docker & Docker Compose
- Envoy proxy for gRPC-Web transcoding
- AWS Cognito for user authentication
- pgAdmin for database management

---

## 📂 Project Structure

```
asante-platform/
│
├── 📱 registration-flow-client/    # React Frontend
│   ├── src/
│   │   ├── api/                    # gRPC service clients
│   │   ├── components/             # React components
│   │   │   ├── signup/             # Registration flow
│   │   │   ├── analytics/          # Dashboard components
│   │   │   └── common/             # Shared components
│   │   ├── user-auth/              # Cognito integration
│   │   └── proto/                  # Generated gRPC-Web files
│   ├── scripts/
│   │   └── generate-proto.sh       # Proto generation script
│   ├── .env.local                  # Local config (not in git)
│   └── package.json
│
├── 🔧 new-grpc-api/                # Python gRPC Backend
│   ├── src/
│   │   ├── services/               # Service implementations
│   │   │   ├── user/               # User service
│   │   │   ├── business/           # Business service
│   │   │   ├── beneficiary/        # Beneficiary service
│   │   │   └── analytics/          # Analytics service
│   │   ├── codegen/                # Generated Python gRPC
│   │   ├── domain/                 # Domain models
│   │   ├── converters/             # DTO converters
│   │   ├── database/               # DB connection
│   │   └── config/                 # Configuration
│   ├── scripts/
│   │   └── generate-proto.sh       # Proto generation script
│   ├── .env                        # Environment config (not in git)
│   ├── requirements.txt            # Python dependencies
│   └── run_all_services.sh         # Start all services
│
├── 🗄️ database_schema_sqlalchemy/  # Database Layer
│   ├── _dev/
│   │   ├── compose.yaml            # Docker Compose config
│   │   ├── .env                    # DB credentials (not in git)
│   │   └── setup-postgres-dev.sh   # Database setup script
│   ├── migrations/
│   │   └── initial_schema/
│   │       └── populate_data.py    # Schema population
│   └── src/
│       └── public/tables/          # SQLAlchemy models
│
├── 🌐 envoy_proxy/                 # Envoy Configuration
│   ├── envoy.yaml                  # Proxy configuration
│   └── docker-compose.yml          # Envoy container setup
│
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## ⚙️ Configuration

### Frontend Environment (.env.local)

Create `registration-flow-client/.env.local`:

```env
# AWS Cognito Configuration
REACT_APP_USER_POOL_ID=your_user_pool_id
REACT_APP_CLIENT_ID=your_client_id
REACT_APP_REGION=your_aws_region

# API Endpoints
REACT_APP_GRPC_ENDPOINT=http://localhost:8080
```

### Backend Environment (.env)

Create `new-grpc-api/.env`:

```env
# Database Configuration
# PostgreSQL Configuration
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=localhost (your hostname & its not effected by docker DNS)
PORT =5432

# pgAdmin Configuration
PGADMIN_DEFAULT_EMAIL=admin_email_
PGADMIN_DEFAULT_PASSWORD=your_admin_password

# Service Ports
USER_SERVICE_PORT=50051
BUSINESS_SERVICE_PORT=50052
BENEFICIARY_SERVICE_PORT=50053
ANALYTICS_SERVICE_PORT=50054
```

### Database Environment (.env)

Create `database_schema_sqlalchemy/_dev/.env`:

```env
# PostgreSQL Configuration
POSTGRES_USER=your_username
PORT=5432
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=localhost(hostname or docker service name if using docker)

# pgAdmin Configuration
PGADMIN_DEFAULT_EMAIL=admin_email_
PGADMIN_DEFAULT_PASSWORD=your_admin_password
```

> ⚠️ **Security Note**: Never commit `.env` files to version control. They contain sensitive credentials and are already in `.gitignore`.

### AWS Cognito Setup

1. Create a User Pool in AWS Cognito
2. Configure app client with no client secret
3. Enable email verification
4. Note your User Pool ID, Client ID, and Region
5. Add these to your frontend `.env.local` file

For detailed Cognito setup, see: [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/)

---

## 🧪 Testing

### Access the Application

1. Navigate to `http://localhost:3000`
2. Click "Create Account" to test registration flow
3. Try both Business and Non-Profit registration paths

### Test User Aliases (Gmail)

Use Gmail's `+` feature to create multiple test accounts:
```
yourname+business1@gmail.com
yourname+business2@gmail.com
yourname+nonprofit1@gmail.com
```

All verification emails arrive at `yourname@gmail.com`.

### Database Access

**pgAdmin Web Interface:**
1. Open `http://localhost:5050`
2. Login with credentials from `.env`
3. Navigate to: Servers → Local Development → Databases → postgres

**Command Line:**
```bash
docker exec -it asante-postgres-dev psql -U asante_dev -d postgres

# List tables
\dt

# Query users
SELECT * FROM users;

# Exit
\q
```

### Service Health Checks

```bash
# Check Envoy proxy
curl http://localhost:9901/ready

# Test gRPC services (requires grpcurl)
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50052 list
grpcurl -plaintext localhost:50053 list
grpcurl -plaintext localhost:50054 list
```

---

## 🔧 Troubleshooting

### Database Won't Start

```bash
cd database_schema_sqlalchemy/_dev
docker-compose down
docker-compose up -d
sleep 30  # Wait for containers to initialize
```

### Database Has No Tables

```bash
cd database_schema_sqlalchemy/migrations/initial_schema
python populate_data.py

# Verify
docker exec -it asante-postgres-dev psql -U asante_dev -d postgres -c "\dt"
```

### Envoy Proxy Issues

```bash
# View logs
docker logs envoy_proxy

# Restart
docker restart envoy_proxy

# Rebuild if needed
cd envoy_proxy
docker-compose down
docker-compose up -d
```

### gRPC Service Errors

**Error**: `ModuleNotFoundError: No module named 'codegen'`

**Solution**: Regenerate protobuf files
```bash
cd new-grpc-api
./scripts/generate-proto.sh
```

**Error**: `503 Service Unavailable`

**Solution**: Ensure all backend services are running
```bash
# Check running services
lsof -i :50051
lsof -i :50052
lsof -i :50053
lsof -i :50054

# Restart services if needed
cd new-grpc-api
./run_all_services.sh
```

### Frontend Build Issues

```bash
cd registration-flow-client

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Regenerate proto files
./scripts/generate-proto.sh
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | Find and kill process: `lsof -ti:PORT \| xargs kill -9` |
| Docker network error | Recreate network: `docker network create asante-network` |
| Proto import errors | Regenerate with `./scripts/generate-proto.sh` |
| Database connection failed | Check Docker containers: `docker ps` |
| Cognito errors | Verify credentials in `.env.local` |

---

## 🛑 Stopping Services

### Stop All Services

```bash
# Stop Docker containers
docker stop envoy_proxy asante-postgres-dev asante-pgadmin

# Stop Python services (Ctrl+C in each terminal)

# Stop React app (Ctrl+C in terminal)
```

### Stop and Clean Up

```bash
# Stop containers
cd database_schema_sqlalchemy/_dev
docker-compose down

cd ../../envoy_proxy
docker-compose down

# Remove Docker network
docker network rm asante-network
```

### Nuclear Option (Remove All Data)

```bash
# WARNING: This deletes all database data
cd database_schema_sqlalchemy/_dev
docker-compose down -v

# Remove all containers and images
docker system prune -a
```

---

## 📚 Documentation

Detailed documentation for each component:

- **[Frontend README](registration-flow-client/README.md)** - React app setup and development
- **[Backend README](new-grpc-api/README.md)** - gRPC services and API reference
- **[Database README](database_schema_sqlalchemy/README.md)** - Database schema and migrations
- **[Envoy Proxy README](envoy_proxy/README.md)** - Proxy configuration and routing

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style and patterns
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all services pass health checks

---

## 📄 License

This project is proprietary and confidential.

---

## 👥 Team

Developed by Asante-CU Boulder Capstone Team

---

## 🙏 Acknowledgments

- AWS Cognito for authentication services
- Envoy Proxy for gRPC-Web transcoding
- SQLAlchemy for ORM capabilities
- Material-UI for React components

---

