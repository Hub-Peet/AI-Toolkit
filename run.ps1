param(
  [string]$App = "app.py"
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
if (-not $root) { $root = Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location $root

Write-Host "[run] Projectmap: $root"

# 1) Controleer venv
$activate = Join-Path $root "venv\Scripts\Activate.ps1"
if (-not (Test-Path $activate)) {
  Write-Warning "Geen venv gevonden. Voer eerst .\\setup.ps1 uit."
  exit 1
}

# 2) Activeer venv
. $activate
Write-Host "[run] venv geactiveerd"

# 3) Controleer secrets
$secrets = Join-Path $root ".streamlit\secrets.toml"
if (-not (Test-Path $secrets) -and -not $env:OPENAI_API_KEY) {
  Write-Warning "Geen OPENAI_API_KEY gevonden (.streamlit\\secrets.toml of omgevingsvariabele)."
}

# 4) Start app
if (-not (Test-Path $App)) {
  Write-Warning "Bestand $App niet gevonden in $root"
  $candidates = Get-ChildItem -Filter "*.py" -File | Select-Object -ExpandProperty Name
  if ($candidates) { Write-Host "Beschikbare .py-bestanden:"; $candidates | ForEach-Object { Write-Host " - $_" } }
  exit 1
}

Write-Host "[run] Start Streamlit: $App"
streamlit run $App
