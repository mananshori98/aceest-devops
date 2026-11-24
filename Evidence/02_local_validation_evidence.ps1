function Show-Cmd($text) { Write-Host "PS> $text" -ForegroundColor Yellow }

Write-Host "=== ASSIGNMENT 2 LOCAL VALIDATION ==="

Write-Host "`n1. PYTHON SYNTAX CHECK"
Show-Cmd ".\.venv\Scripts\python.exe -m py_compile .\app.py"
.\.venv\Scripts\python.exe -m py_compile .\app.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "Syntax check: PASSED" -ForegroundColor Green
}

Write-Host "`n2. EXPANDED PYTEST SUITE AND COVERAGE"
Show-Cmd ".\.venv\Scripts\python.exe -m pytest -q --cov=app --cov-report=term"
.\.venv\Scripts\python.exe -m pytest -q --cov=app --cov-report=term

Write-Host "`n3. FILES CHANGED SINCE ASSIGNMENT 1 BASELINE"
Show-Cmd "git diff --name-status assignment-1-final HEAD"
git diff --name-status assignment-1-final HEAD
