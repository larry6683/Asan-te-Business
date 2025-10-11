# Business Registration Flow - Setup Guide

Complete setup instructions for the business registration application with gRPC backend, PostgreSQL database, and React frontend.

---

## 📋 Prerequisites

Ensure you have the following installed:
- **Docker Desktop** (running)
- **Node.js** (v16 or higher)
- **npm** or **yarn**
- **Python 3.8+** (with pip)
- **Git**

---

## 🚀 Quick Start

### 1. Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Install frontend dependencies
cd registration-flow-client
npm install
cd ..

# Install backend Python dependencies
cd new-grpc-api
pip install grpcio grpcio-tools psycopg2-binary sqlalchemy
cd ..
```

### 2. Set Up Docker Network

```bash
docker network create asante-network
```

### 3. Start PostgreSQL Database

```bash
cd database_schema_sqlalchemy/_dev
bash setup-postgres-dev.sh
# When prompted, choose 'y' to start containers
```

**Wait 30 seconds for containers to fully start:**
```bash
sleep 30
```

**Database will be running on:**
- PostgreSQL: `localhost:5432`
- pgAdmin: `http://localhost:5050`

**Credentials (from `.env` file):**
- DB User: `asante_dev`
- DB Password: `password`
- pgAdmin Email: `admin@asante.com`
- pgAdmin Password: `AdminPass123!`

### 3.1. Configure pgAdmin (First Time Setup - Do This Once)

1. Open browser to `http://localhost:5050`
2. Login with:
   - **Email:** `admin@asante.com`
   - **Password:** `AdminPass123!`
3. **Right-click** on "Servers" in left sidebar
4. Click **"Register" → "Server..."**
5. **General tab:**
   - Name: `Local Development` (or any name)
6. **Connection tab** - Enter these EXACT values:
   - **Host name/address:** `postgres` (⚠️ NOT localhost!)
   - **Port:** `5432`
   - **Maintenance database:** `postgres`
   - **Username:** `asante_dev`
   - **Password:** `password`
   - ✅ Check "Save password"
7. Click **"Save"**

You should now see the server connected in the left sidebar.

### 3.2. Populate Database Tables

```bash
# Go to migrations directory
cd database_schema_sqlalchemy/migrations/initial_schema

# Run population script
python populate_data.py

# Verify tables were created (should show 26 tables)
docker exec -it asante-postgres-dev psql -U asante_dev -d postgres -c "\dt"
```

**Expected output:** List of 26 tables including `users`, `businesses`, `beneficiaries`, etc.

### 4. Start Envoy Proxy

```bash
cd envoy_proxy
docker run -d --name envoy_proxy \
  --network asante-network \
  -p 8080:8080 \
  -p 9901:9901 \
  -v $(pwd)/envoy.yaml:/etc/envoy/envoy.yaml \
  envoyproxy/envoy:v1.27-latest
```

**Envoy will be running on:**
- Proxy: `localhost:8080`
- Admin: `localhost:9901`

### 5. Generate Protobuf Files (Backend - Python)

**This must be done before starting the backend services!**

```bash
cd new-grpc-api

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Make the generation script executable
chmod +x scripts/generate-proto.sh

# Generate Python protobuf files
./scripts/generate-proto.sh
```

**Expected output:**
```
🔧 Generating Python protobuf files...
✅ Protobuf files generated
🔧 Fixing import paths...
✅ Import paths fixed
✅ Complete!
```

**What this does:**
- Generates Python code from `.proto` files
- Fixes import paths for proper module resolution
- Creates necessary `__init__.py` files

### 6. Generate Protobuf Files (Frontend - JavaScript)

```bash
cd registration-flow-client

# Make the generation script executable (if not already)
chmod +x scripts/generate-proto.sh

# Generate JavaScript protobuf files
./scripts/generate-proto.sh
```

**Expected output:**
```
🔧 Generating JavaScript code from proto files...
✅ Generated files:
✅ Proto generation complete!
```

### 7. Start gRPC Backend Services (Python)

Open **3 separate terminals** and run each command in its own terminal:

**Terminal 1 - User Service:**
```bash
cd new-grpc-api
chmod +x run_user_service.sh
./run_user_service.sh
```

**Terminal 2 - Business Service:**
```bash
cd new-grpc-api
chmod +x run_business_service.sh
./run_business_service.sh
```

**Terminal 3 - Beneficiary Service:**
```bash
cd new-grpc-api
chmod +x run_beneficiary_service.sh
./run_beneficiary_service.sh
```

**Services will be running on:**
- User Service: `localhost:50051`
- Business Service: `localhost:50052`
- Beneficiary Service: `localhost:50053`

**✅ You should see output like:**
```
Starting User Service on port 50051...
User service listening on [::]:50051
```

**⚠️ Keep these terminals open** - the services need to keep running!

### 8. Start React Frontend

**Open a 4th terminal:**

```bash
cd registration-flow-client
npm start
```

**Frontend will open at:** `http://localhost:3000`

---

## 🖥️ Terminal Setup Summary

You should have **6 terminals open** in total:

1. **PostgreSQL/Docker** - Shows Docker container logs (optional to keep open)
2. **Envoy Proxy** - Running in Docker (background)
3. **User Service** - `./run_user_service.sh` (keep open)
4. **Business Service** - `./run_business_service.sh` (keep open)
5. **Beneficiary Service** - `./run_beneficiary_service.sh` (keep open)
6. **React App** - `npm start` (keep open)

**Quick tip:** Use a terminal multiplexer like `tmux` or `iTerm2` split panes to manage multiple terminals easily.

---

## 🔐 AWS Cognito Configuration

The app uses AWS Cognito for authentication with the following configuration:

See TJs message

**Frontend environment variables are in:** `registration-flow-client/.env.local` (create if missing)

**Backend configuration is in:** `new-grpc-api/src/config/` or environment variables

> ⚠️ **Important:** These config files contain sensitive credentials and are in `.gitignore`. Do not commit them to source control.

---

## 🧪 Testing the Application

### Sign Up Flow

1. Go to `http://localhost:3000`
2. Click "Create Account"
3. Select "Business" or "Non-Profit"
4. Enter email and password (use email aliases for testing: `your.email+b01@gmail.com`)
5. Check email for verification code
6. Enter verification code
7. Select causes (minimum 3 for business, or 1 primary + up to 2 supporting for non-profit)
8. Select business/non-profit size
9. Fill out business/non-profit information
10. Click "Access Portal"

### Sign In Flow

1. Go to `http://localhost:3000`
2. Click "Log In"
3. Enter registered email and password
4. Should redirect to portal (or registration if incomplete)

### Testing Email Aliases

Use Gmail's `+` feature to create multiple test accounts with one email:
- `yourname+b01@gmail.com` (business #1)
- `yourname+b02@gmail.com` (business #2)
- `yourname+np01@gmail.com` (non-profit #1)

All verification emails go to `yourname@gmail.com`.

---

## 🗄️ Database Access

### Using pgAdmin (Already Configured in Step 3.1)

1. Open `http://localhost:5050`
2. Login with credentials from step 3
3. Expand: **Servers → Local Development → Databases → postgres → Schemas → public → Tables**

### Using Command Line (Quick Check)

```bash
# Connect to database
docker exec -it asante-postgres-dev psql -U asante_dev -d postgres

# List all tables
\dt

# View table data (example)
SELECT * FROM users;

# Exit
\q
```

### Key Tables

- **users** - User accounts from Cognito
- **businesses** - Registered businesses
- **beneficiaries** - Registered non-profits
- **business_causes** - Business cause selections
- **beneficiary_causes** - Non-profit cause selections

---

## 🏗️ Architecture Overview

```
┌─────────────┐
│   React     │ :3000
│  Frontend   │
└──────┬──────┘
       │
       ↓ gRPC-Web
┌─────────────┐
│    Envoy    │ :8080
│    Proxy    │
└──────┬──────┘
       │
       ↓ gRPC
┌─────────────────────────────┐
│  Python gRPC Services       │
│  • UserService      :50051  │
│  • BusinessService  :50052  │
│  • BeneficiaryService :50053│
└──────┬──────────────────────┘
       │
       ↓
┌─────────────┐
│ PostgreSQL  │ :5432
│  Database   │
└─────────────┘

Authentication: AWS Cognito
```

---

## 🔧 Troubleshooting

### Database Won't Start

```bash
cd database_schema_sqlalchemy/_dev
docker compose down
docker compose up -d
sleep 30  # Wait for startup
```

### Database Has No Tables

```bash
# Populate the database
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

# If port conflict, stop and remove
docker stop envoy_proxy
docker rm envoy_proxy
# Then run the start command again from step 4
```

### Python Proto Generation Issues

**Error:** `ModuleNotFoundError: No module named 'error'`

**Solution:**
```bash
cd new-grpc-api

# Regenerate proto files with fixed imports
./scripts/generate-proto.sh

# Use the runner scripts (not direct python commands)
./run_user_service.sh  # ✅ Correct
# NOT: python src/services/user/server.py  # ❌ Wrong
```

**Why this happens:**
- The `protoc` compiler generates imports like `from error import error_pb2`
- Our script fixes them to `from codegen.error import error_pb2`
- The runner scripts set `PYTHONPATH` correctly for module resolution

### gRPC Service Won't Start

**Error:** `Permission denied`

**Solution:**
```bash
cd new-grpc-api
chmod +x run_user_service.sh
chmod +x run_business_service.sh
chmod +x run_beneficiary_service.sh
```

**Check if services are running:**
```bash
lsof -i :50051  # User Service
lsof -i :50052  # Business Service  
lsof -i :50053  # Beneficiary Service
```

### Python Dependencies Missing

```bash
# Install required packages
cd new-grpc-api
pip install grpcio grpcio-tools psycopg2-binary sqlalchemy
```

### Frontend Issues

```bash
# Clear cache and reinstall
cd registration-flow-client
rm -rf node_modules package-lock.json
npm install
npm start
```

### "User not found" Error After Sign-In

This was fixed by creating the user in the database after Cognito sign-up. If you still see this:
1. Check that UserService is running on port 50051: `lsof -i :50051`
2. Verify database connection in Python service
3. Check Python service logs in the terminal

### Session/Cookie Issues

If logged-in users are redirected to registration:
1. Check browser cookies for `asanteApp`
2. Verify `userApiService.js` correctly reads from cookies
3. Check console for relationship detection logs

---

## 📁 Project Structure

```
project-root/
├── registration-flow-client/     # React frontend
│   ├── src/
│   │   ├── api/                  # gRPC service clients
│   │   ├── components/           # React components
│   │   ├── user-auth/           # Cognito authentication
│   │   └── proto/               # Generated gRPC files
│   ├── scripts/
│   │   └── generate-proto.sh    # JS proto generation
│   ├── .env.local               # Local config (not committed)
│   └── package.json
│
├── new-grpc-api/                # Python gRPC backend
│   ├── src/
│   │   ├── services/
│   │   │   ├── user/server.py
│   │   │   ├── business/server.py
│   │   │   └── beneficiary/server.py
│   │   └── protos/              # Proto definitions
│   ├── scripts/
│   │   └── generate-proto.sh    # Python proto generation
│   ├── run_user_service.sh
│   ├── run_business_service.sh
│   ├── run_beneficiary_service.sh
│   └── requirements.txt         # Python dependencies
│
├── database_schema_sqlalchemy/  # Database setup
│   ├── _dev/
│   │   ├── compose.yaml         # Docker Compose config
│   │   ├── .env                 # DB credentials
│   │   └── setup-postgres-dev.sh
│   └── migrations/
│       └── initial_schema/
│           └── populate_data.py
│
└── envoy-proxy/
    └── envoy.yaml              # Proxy configuration
```

---

## 🛑 Stopping Services

### Stop Everything

```bash
# Stop Docker containers
docker stop envoy_proxy
cd database_schema_sqlalchemy/_dev
docker compose down

# Stop Python services (Ctrl+C in each terminal)
# Stop React app (Ctrl+C in terminal)
```

### Stop Without Losing Data

```bash
# Keeps database data in volumes
cd database_schema_sqlalchemy/_dev
docker compose stop
```

### Stop and Remove All Data

```bash
# WARNING: This deletes all database data
cd database_schema_sqlalchemy/_dev
docker compose down -v
```

---

## 🔐 Security Notes

**Never commit these files:**
- `registration-flow-client/.env.local`
- `new-grpc-api/src/config/*.json` (if they contain credentials)
- `database_schema_sqlalchemy/_dev/.env`

They are already in `.gitignore` and contain sensitive credentials.

---

## ✅ Success Checklist

- [ ] Docker network created (`asante-network`)
- [ ] PostgreSQL running and accessible at `localhost:5432`
- [ ] pgAdmin configured and connected to database at `http://localhost:5050`
- [ ] Database populated with 26 tables
- [ ] Envoy proxy running on port 8080
- [ ] **Backend protobuf files generated** (`./scripts/generate-proto.sh` in `new-grpc-api`)
- [ ] **Frontend protobuf files generated** (`./scripts/generate-proto.sh` in `registration-flow-client`)
- [ ] All 3 Python gRPC services running (50051, 50052, 50053)
- [ ] React app running on port 3000
- [ ] Can sign up with new email
- [ ] Receive and enter verification code
- [ ] Can complete registration flow
- [ ] Business/non-profit saved to database
- [ ] Can log in with registered account
- [ ] Redirects to portal (or shows portal URL)

---

## 📞 Need Help?

Common issues and solutions are in the Troubleshooting section above. 

**Check logs:**
- Browser Console: Press F12
- Docker logs: `docker logs <container-name>`
- Backend logs: Check terminals where Python services are running

---

## 🎉 You're Ready!

Once all services are running and the checklist is complete, your development environment is ready for testing the complete business registration flow.