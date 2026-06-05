$Source = "E:\python_Demo\paper-polish-agent"
$Output = "E:\python_Demo\paper-polish-agent-deploy.zip"

if (Test-Path $Output) {
    Remove-Item -LiteralPath $Output -Force
}

$excludePatterns = @(
    "\\.git\\",
    "\\.idea\\",
    "\\.venv\\",
    "\\frontend\\node_modules\\",
    "\\frontend\\dist\\",
    "\\backend\\.env$",
    "\\backend\\.pytest_cache\\",
    "__pycache__",
    "\\.codex_tmp\\"
)

$files = Get-ChildItem -LiteralPath $Source -Recurse -File | Where-Object {
    $path = $_.FullName
    -not ($excludePatterns | Where-Object { $path -match $_ })
}

Compress-Archive -LiteralPath $files.FullName -DestinationPath $Output -Force
Write-Host "Created $Output"
