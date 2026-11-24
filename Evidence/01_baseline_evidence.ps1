function Show-Cmd($text) { Write-Host "PS> $text" -ForegroundColor Yellow }

Write-Host "=== ASSIGNMENT 2 BASELINE EVIDENCE ==="

Write-Host "`n1. CURRENT WORKING BRANCH"
Show-Cmd "git branch --show-current"
git branch --show-current

Write-Host "`n2. BASELINE TEST RESULT (assignment-1-final)"
$py = "$PWD\.venv\Scripts\python.exe"; $t = "$env:TEMP\base1"
Show-Cmd "git worktree add `$env:TEMP\base1 assignment-1-final"
git worktree add $t assignment-1-final 2>&1 | Out-Null
Show-Cmd "cd `$env:TEMP\base1"
Push-Location $t
Show-Cmd "$py -m pytest -q"
& $py -m pytest -q
Pop-Location
Show-Cmd "git worktree remove `$env:TEMP\base1 --force"
git worktree remove $t --force

Write-Host "`n3. CREATED BRANCHES"
Show-Cmd "git branch"
git branch

Write-Host "`n4. ASSIGNMENT 1 BASELINE TAG"
Show-Cmd 'git tag --list "assignment-1-final"'
git tag --list "assignment-1-final"

Write-Host "`n5. REPOSITORY STATUS"
Show-Cmd "git status"
git status
