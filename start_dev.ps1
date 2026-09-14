# start_dev.ps1

Write-Host "Starting AI Receptionist Development Servers..." -ForegroundColor Cyan

# Start the FastAPI Backend in a new PowerShell window
Write-Host "Launching Backend (FastAPI)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd apps\api; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

# Start the Next.js Frontend in a new PowerShell window
Write-Host "Launching Frontend (Next.js)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd apps\web; npm run dev"

Write-Host "Both servers are starting in separate windows!" -ForegroundColor Green
Write-Host "Backend API will be available at: http://localhost:8000/docs"
Write-Host "Frontend Dashboard will be available at: http://localhost:3000"
