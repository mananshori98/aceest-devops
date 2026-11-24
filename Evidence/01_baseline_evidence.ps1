Write-Host "=== ASSIGNMENT 2 BASELINE EVIDENCE ==="
Write-Host "`n1. CURRENT WORKING BRANCH";    git branch --show-current
Write-Host "`n2. BASELINE TEST RESULT (assignment-1-final)"
$py = "$PWD\.venv\Scripts\python.exe"; $t = "$env:TEMP\base1"
git worktree add $t assignment-1-final 2>&1 | Out-Null
Push-Location $t; & $py -m pytest -q; Pop-Location
git worktree remove $t --force
Write-Host "`n3. CREATED BRANCHES";          git branch
Write-Host "`n4. ASSIGNMENT 1 BASELINE TAG"; git tag --list "assignment-1-final"
Write-Host "`n5. REPOSITORY STATUS";         git status
