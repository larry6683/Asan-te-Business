# Business Registration Flow - Setup Guide

Complete setup instructions for the business registration application with gRPC backend, PostgreSQL database, and React frontend.

---

## Prerequisites

Ensure you have the following installed:
- **Docker Desktop** (running)
- **Node.js** (v16 or higher)
- **npm** or **yarn**
- **.NET SDK** (6.0 or higher)
- **Git**

---

## Quick Start

### 1. Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Install frontend dependencies
cd registration-flow-client
npm install
cd ..

# Restore backend dependencies
cd new-grpc-api
dotnet restore
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

**Database will be running on:**
- PostgreSQL: `localhost:5432`
- pgAdmin: `http://localhost:5050`

**Credentials (from `.env` file):**
- DB User: `asante_dev`
- DB Password: `password`
- pgAdmin Email: `admin@asante.com`
- pgAdmin Password: `AdminPass123!`

### 4. Start Envoy Proxy

```bash
cd envoy-proxy
docker run -d --name envoy-proxy \
  --network asante-network \
  -p 8080:8080 \
  -p 9901:9901 \
  -v $(pwd)/envoy.yaml:/etc/envoy/envoy.yaml \
  envoyproxy/envoy:v1.27-latest
```

**Envoy will be running on:**
- Proxy: `localhost:8080`
- Admin: `localhost:9901`

### 5. Start gRPC Backend Services

Open **3 separate terminals** and run:

```bash
# Terminal 1 - User Service
cd new-grpc-api
dotnet run --project UserService

# Terminal 2 - Business Service  
cd new-grpc-api
dotnet run --project BusinessService

# Terminal 3 - Beneficiary Service
cd new-grpc-api
dotnet run --project BeneficiaryService
```

**Services will be running on:**
- User Service: `localhost:50051`
- Business Service: `localhost:50052`
- Beneficiary Service: `localhost:50053`

### 6. Start React Frontend

```bash
cd registration-flow-client
npm start
```

**Frontend will open at:** `http://localhost:3000`

---

## AWS Cognito Configuration

The app uses AWS Cognito for authentication with the following configuration:

- **User Pool ID:** 
- **Client ID:** 
- **Region:** 

**Frontend environment variables are in:** `registration-flow-client/.env.local`

**Backend configuration is in:** `new-grpc-api/appsettings.development.json`

> ⚠️ **Important:** These config files contain sensitive credentials and are in `.gitignore`. Do not commit them to source control.

---

## Testing the Application

### Sign Up Flow

1. Go to `http://localhost:3000`
2. Click "Create Account"
3. Select "Business"
4. Enter email and password (use email aliases for testing: `your.email+b01@gmail.com`)
5. Check email for verification code
6. Enter verification code
7. Select causes (minimum 3 for business, or 1 primary + up to 2 supporting for non-profit)
8. Select business size
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

### Using pgAdmin (Web UI)

1. Open `http://localhost:5050`
2. Login with credentials above
3. Right-click "Servers" → "Register" → "Server"
4. **General tab:** Name: `Local Development`
5. **Connection tab:**
   - Host: `postgres`
   - Port: `5432`
   - Database: `postgres`
   - Username: `asante_dev`
   - Password: `password`
6. Click "Save"

### Key Tables

- **users** - User accounts from Cognito
- **businesses** - Registered businesses
- **beneficiaries** - Registered non-profits
- **business_causes** - Business cause selections
- **beneficiary_causes** - Non-profit cause selections

---

## 🛠️ Architecture Overview

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
│  gRPC Services              │
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
```

### Envoy Proxy Issues

```bash
# View logs
docker logs envoy-proxy

# Restart
docker restart envoy-proxy

# If port conflict, stop and remove
docker stop envoy-proxy
docker rm envoy-proxy
# Then run the start command again
```

### gRPC Service Not Responding

```bash
# Check if services are running
netstat -an | grep 5005  # Should show ports 50051, 50052, 50053

# Restart specific service
cd new-grpc-api
dotnet run --project <ServiceName>
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
1. Check `signupUser.js` includes the database user creation
2. Verify UserService is running on port 50051

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
│   ├── .env.local               # Local config (not committed)
│   └── package.json
│
├── new-grpc-api/                # .NET gRPC backend
│   ├── UserService/
│   ├── BusinessService/
│   ├── BeneficiaryService/
│   └── appsettings.development.json  # Local config (not committed)
│
├── database_schema_sqlalchemy/  # Database setup
│   └── _dev/
│       ├── compose.yaml         # Docker Compose config
│       ├── .env                 # DB credentials
│       └── setup-postgres-dev.sh
│
└── envoy-proxy/
    └── envoy.yaml              # Proxy configuration
```

---

## Stopping Services

### Stop Everything

```bash
# Stop Docker containers
docker stop envoy-proxy
cd database_schema_sqlalchemy/_dev
docker compose down

# Stop .NET services (Ctrl+C in each terminal)
# Stop React app (Ctrl+C in terminal)
```

### Stop Without Losing Data

```bash
# Keeps database data in volumes
docker compose stop
```

### Stop and Remove All Data

```bash
# WARNING: This deletes all database data
docker compose down -v
```

---

## Security Notes

**Never commit these files:**
- `registration-flow-client/.env.local`
- `new-grpc-api/appsettings.development.json`
- `database_schema_sqlalchemy/_dev/.env`

They are already in `.gitignore` and contain sensitive credentials.

---

## Success Checklist

- [ ] Docker network created
- [ ] PostgreSQL running and accessible
- [ ] Envoy proxy running on port 8080
- [ ] All 3 gRPC services running
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
- Backend logs: Check terminal where services are running

---


Once all services are running and the checklist is complete, your development environment is ready for testing the complete business registration flow.