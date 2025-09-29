# gRPC API Services

Clean implementation of gRPC services for User, Business, and Beneficiary management.

## Structure

\\\
new-grpc-api/
├── src/
│   ├── protos/              # Protocol buffer definitions
│   ├── codegen/             # Generated gRPC code
│   ├── services/            # Service implementations
│   ├── domain/              # Domain models
│   ├── converters/          # DB to domain converters
│   ├── database/            # Database connection
│   ├── config/              # Configuration
│   └── utils/               # Utilities
├── requirements.txt         # Python dependencies
├── run_all_services.ps1     # Start all services
├── test_services.py         # Test script
└── docker-compose.yml       # Docker configuration
\\\

## Services

- **User Service** (port 50051)
  - GetUser(email) → User
  - CreateUser(email, user_type, mailing_list_signup) → User

- **Business Service** (port 50052)
  - GetBusiness(business_id) → Business
  - CreateBusiness(...) → Business

- **Beneficiary Service** (port 50053)
  - GetBeneficiary(beneficiary_id) → Beneficiary
  - CreateBeneficiary(...) → Beneficiary

## Setup

1. **Install Dependencies**
   \\\powershell
   pip install -r requirements.txt
   \\\

2. **Ensure Database is Running**
   \\\powershell
   cd ../database_schema_sqlalchemy/_dev
   bash ./setup-postgres-dev.sh
   bash ./setup_schema.sh
   \\\

3. **Generate gRPC Code** (if proto files changed)
   \\\powershell
   cd src
   python -m grpc_tools.protoc --proto_path=protos --python_out=codegen --grpc_python_out=codegen --pyi_out=codegen error/error.proto
   python -m grpc_tools.protoc --proto_path=protos --python_out=codegen --grpc_python_out=codegen --pyi_out=codegen user/user.proto
   python -m grpc_tools.protoc --proto_path=protos --python_out=codegen --grpc_python_out=codegen --pyi_out=codegen business/business.proto
   python -m grpc_tools.protoc --proto_path=protos --python_out=codegen --grpc_python_out=codegen --pyi_out=codegen beneficiary/beneficiary.proto
   cd ..
   python fix_imports.py
   \\\

## Running

### Option 1: PowerShell Script (Recommended)
\\\powershell
./run_all_services.ps1
\\\

### Option 2: Manual Start
\\\powershell
$env:PYTHONPATH = '$PWD/src'

# Terminal 1
python src/services/user/server.py

# Terminal 2
python src/services/business/server.py

# Terminal 3
python src/services/beneficiary/server.py
\\\

### Option 3: Docker
\\\powershell
docker-compose up --build
\\\

## Testing

\\\powershell
$env:PYTHONPATH = '$PWD/src'
python test_services.py
\\\

## API Examples

### Create User
\\\python
import grpc
from codegen.user import user_pb2, user_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = user_pb2_grpc.UserServiceStub(channel)

response = stub.CreateUser(user_pb2.CreateUserRequest(
    email='john@example.com',
    user_type='BUSINESS',
    mailing_list_signup=True
))
\\\

### Get User
\\\python
response = stub.GetUser(user_pb2.GetUserRequest(
    email='john@example.com'
))
\\\

### Create Business
\\\python
from codegen.business import business_pb2, business_pb2_grpc

channel = grpc.insecure_channel('localhost:50052')
stub = business_pb2_grpc.BusinessServiceStub(channel)

response = stub.CreateBusiness(business_pb2.CreateBusinessRequest(
    business_name='Acme Corp',
    email='info@acme.com',
    location_city='Denver',
    location_state='CO',
    business_size='MEDIUM',
    user_email='john@example.com'
))
\\\

## Error Handling

All responses include an \rrors\ field:

\\\python
if response.errors:
    for error in response.errors:
        print(f'{error.code}: {error.message} - {error.detail}')
else:
    print(f'Success: {response.user.id}')
\\\

## Environment Variables

Create \.env\ file:
\\\
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=asante_dev
DB_PASSWORD=password
\\\

## Troubleshooting

### Import Errors
Make sure PYTHONPATH is set:
\\\powershell
$env:PYTHONPATH = '$PWD/src'
\\\

### Database Connection Errors
Ensure PostgreSQL is running and credentials are correct in .env file.

### gRPC Connection Errors
Check that services are running on correct ports (50051, 50052, 50053).
