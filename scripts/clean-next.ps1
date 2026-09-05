$ErrorActionPreference = 'Stop'

$workspace = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$target = [System.IO.Path]::GetFullPath((Join-Path $workspace '.next'))

if (-not $target.StartsWith($workspace, [System.StringComparison]::OrdinalIgnoreCase) -or
    [System.IO.Path]::GetFileName($target) -ne '.next') {
    throw 'Refusing to remove an unsafe cache path.'
}

if (Test-Path -LiteralPath $target) {
    Remove-Item -LiteralPath $target -Recurse -Force
    Write-Host 'Cleared the generated Next.js cache.'
}
