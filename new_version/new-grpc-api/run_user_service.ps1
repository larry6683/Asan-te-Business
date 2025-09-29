$env:PYTHONPATH = "$PWD/src"
Write-Host 'Starting User Service on port 50051...' -ForegroundColor Cyan
python src/services/user/server.py
