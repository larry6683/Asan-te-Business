$env:PYTHONPATH = "$PWD/src"
Write-Host 'Starting Beneficiary Service on port 50053...' -ForegroundColor Cyan
python src/services/beneficiary/server.py
