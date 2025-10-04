$env:PYTHONPATH = "$PWD/src"
Write-Host 'Starting Business Service on port 50052...' -ForegroundColor Cyan
python src/services/business/server.py
