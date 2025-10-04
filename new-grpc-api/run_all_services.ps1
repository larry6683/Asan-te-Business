$ErrorActionPreference = 'Stop'

Write-Host '========================================' -ForegroundColor Blue
Write-Host 'Starting All gRPC Services' -ForegroundColor Blue
Write-Host '========================================' -ForegroundColor Blue
Write-Host ''

# Set PYTHONPATH
$env:PYTHONPATH = "$PWD/src"

# Start services in background
Write-Host 'Starting User Service (port 50051)...' -ForegroundColor Yellow
Start-Process powershell -ArgumentList '-NoExit', '-Command', 
    "$env:PYTHONPATH="$PWD/src"; cd "$PWD"; python src/services/user/server.py"

Start-Sleep -Seconds 2

Write-Host 'Starting Business Service (port 50052)...' -ForegroundColor Yellow
Start-Process powershell -ArgumentList '-NoExit', '-Command', 
    "$env:PYTHONPATH="$PWD/src"; cd "$PWD"; python src/services/business/server.py"

Start-Sleep -Seconds 2

Write-Host 'Starting Beneficiary Service (port 50053)...' -ForegroundColor Yellow
Start-Process powershell -ArgumentList '-NoExit', '-Command', 
    "$env:PYTHONPATH="$PWD/src"; cd "$PWD"; python src/services/beneficiary/server.py"

Start-Sleep -Seconds 3

Write-Host ''
Write-Host '========================================' -ForegroundColor Green
Write-Host '✓ All services started successfully!' -ForegroundColor Green
Write-Host '========================================' -ForegroundColor Green
Write-Host ''
Write-Host 'Services running on:' -ForegroundColor Cyan
Write-Host '  User Service:        localhost:50051' -ForegroundColor White
Write-Host '  Business Service:    localhost:50052' -ForegroundColor White
Write-Host '  Beneficiary Service: localhost:50053' -ForegroundColor White
Write-Host ''
Write-Host 'gRPC Reflection is enabled on all services.' -ForegroundColor Yellow
Write-Host 'You can now test with Postman or any gRPC client.' -ForegroundColor Yellow
Write-Host ''
Write-Host 'To stop all services, close this window and all service windows.' -ForegroundColor Gray
Write-Host ''
Write-Host 'Press any key to exit this launcher...' -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
