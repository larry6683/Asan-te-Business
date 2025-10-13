# Envoy Proxy for gRPC-Web

This Envoy proxy enables your React frontend (running in browsers) to communicate with your gRPC services.

## What This Does

Envoy acts as a translator between:
- **Frontend**: React app using gRPC-Web (browser-compatible)
- **Backend**: Python gRPC services (native gRPC)

```
React (localhost:3000) → Envoy (localhost:8080) → gRPC Services (50051-50053)
```

## Why You Need This

Browsers cannot make native gRPC calls (HTTP/2 with gRPC framing). Envoy translates browser-friendly gRPC-Web requests into native gRPC calls that your Python services understand.

This is the equivalent of what AWS API Gateway did for your old REST API.

## Prerequisites

- Docker Desktop installed and running
- Your gRPC services running (ports 50051, 50052, 50053)
- Docker network `asante-network` created

## Quick Start

### 1. Create Docker Network (if not already created)

```bash
docker network create --driver bridge asante-network
```

### 2. Start Envoy Proxy

```bash
# From the envoy-proxy directory
docker-compose up
```

Or run Envoy directly:

```bash
docker run -d \
  --name envoy-proxy \
  --network asante-network \
  -p 8080:8080 \
  -p 9901:9901 \
  -v $(pwd)/envoy.yaml:/etc/envoy/envoy.yaml \
  envoyproxy/envoy:v1.28-latest
```

### 3. Verify Envoy is Running

```bash
# Check Envoy admin interface
curl http://localhost:9901/ready

# Should return: LIVE
```

### 4. Test gRPC-Web Connection

Once your React frontend is set up, it will call:
```
http://localhost:8080/user.UserService/CreateUser
http://localhost:8080/business.BusinessService/CreateBusiness
http://localhost:8080/beneficiary.BeneficiaryService/CreateBeneficiary
```

## Ports

- **8080**: gRPC-Web endpoint (React frontend calls this)
- **9901**: Envoy admin interface (for health checks)

## Architecture

```
┌─────────────────────────────────────────┐
│  React Frontend (Port 3000)             │
│  Uses: grpc-web JavaScript library      │
└─────────────────────────────────────────┘
              ↓ HTTP/1.1 (gRPC-Web)
┌─────────────────────────────────────────┐
│  Envoy Proxy (Port 8080)                │
│  Translates: gRPC-Web → native gRPC     │
└─────────────────────────────────────────┘
              ↓ HTTP/2 (native gRPC)
┌─────────────────────────────────────────┐
│  gRPC Services                          │
│  - User Service (50051)                 │
│  - Business Service (50052)             │
│  - Beneficiary Service (50053)          │
└─────────────────────────────────────────┘
```

## Configuration

The `envoy.yaml` file configures:

1. **Listener (Port 8080)**: Accepts gRPC-Web requests from browsers
2. **Routes**: Maps service names to backend gRPC services
3. **Clusters**: Defines backend gRPC service addresses
4. **Filters**: Includes gRPC-Web and CORS filters
5. **CORS**: Allows cross-origin requests from React dev server

## Troubleshooting

### Envoy won't start
```bash
# Check if ports are already in use
lsof -i :8080
lsof -i :9901

# Check Docker logs
docker-compose logs envoy
```

### Cannot connect to gRPC services
```bash
# Make sure gRPC services are running
# From new-grpc-api folder:
./run_all_services.ps1

# Or manually check if services are up:
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50052 list
grpcurl -plaintext localhost:50053 list
```

### CORS errors in browser
Check that Envoy's CORS configuration includes your React dev server origin:
```yaml
allow_origin_string_match:
  - prefix: "*"  # Allows all origins (development only!)
```

For production, specify exact origins:
```yaml
allow_origin_string_match:
  - exact: "https://yourapp.com"
```

## Stopping Envoy

```bash
# Stop with docker-compose
docker-compose down

# Or stop container directly
docker stop envoy-proxy
docker rm envoy-proxy
```

## Next Steps

Once Envoy is running:

1. Set up your React frontend with grpc-web package
2. Generate JavaScript gRPC-Web client code from your .proto files
3. Update React API calls to use gRPC-Web clients
4. Point React to `http://localhost:8080` as the gRPC endpoint

## Notes

- Envoy runs in a Docker container on the same network as your gRPC services
- The container uses `host.docker.internal` to reach services on your host machine
- In production, this would be deployed alongside your services in AWS/cloud
- The current configuration is for **development only** (permissive CORS)

## Health Check Endpoints

- `http://localhost:9901/ready` - Check if Envoy is ready
- `http://localhost:9901/stats` - View Envoy statistics
- `http://localhost:9901/clusters` - View backend cluster health