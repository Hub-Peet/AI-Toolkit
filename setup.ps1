param(
  [string]$Key = "",
  [switch]$Start,
  [string]$App = "app.py"
)

$ErrorActionPreference = "Stop"

# Bepaal projectroot (map van dit script) en ga daarheen
$root = $PSScriptRoot
if (-not $root) { $root = Split-Path -Parent $MyInvocation.MyCommand.Path }
Set-Location $root

Write-Host "[setup] Projectmap: $root"

# 1) Controleer Python
try {
  $ver = & python --version
  Write-Host "[setup] Python gevonden: $ver"
} catch {
  Write-Error "Python niet gevonden in PATH. Installeer Python 3.x en start PowerShell opnieuw."
}

# 2) Virtuele omgeving
if (-not (Test-Path ".\venv")) {
  Write-Host "[setup] Maak venv..."
  python -m venv venv
} else {
  Write-Host "[setup] venv bestaat al"
}

# 3) Activeer venv (dot-source, zodat de env in huidige sessie blijft)
$activate = Join-Path $root "venv\Scripts\Activate.ps1"
if (-not (Test-Path $activate)) { Write-Error "Kon venv activatiescript niet vinden: $activate" }
. $activate
Write-Host "[setup] venv geactiveerd"

# 4) requirements.txt (aanmaken indien ontbreekt)
if (-not (Test-Path ".\requirements.txt")) {
  Write-Host "[setup] Schrijf requirements.txt"
  @"
streamlit
openai
python-docx
"@ | Set-Content -Path ".\requirements.txt" -Encoding UTF8
} else {
  Write-Host "[setup] requirements.txt bestaat al"
}

# 5) Dependencies installeren
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 6) Secrets (.streamlit/secrets.toml)
$secretsDir = ".\.streamlit"
$secretsFile = Join-Path $secretsDir "secrets.toml"
if (-not (Test-Path $secretsDir)) { New-Item -ItemType Directory -Path $secretsDir | Out-Null }

if (-not (Test-Path $secretsFile)) {
  if (-not $Key) {
    if ($env:OPENAI_API_KEY) { $Key = $env:OPENAI_API_KEY }
    else { $Key = Read-Host -Prompt "Voer je OPENAI_API_KEY in (sk-...)" }
  }
  "OPENAI_API_KEY = `"$Key`"" | Set-Content -Path $secretsFile -Encoding UTF8
  Write-Host "[setup] secrets.toml geschreven"
} else {
  Write-Host "[setup] secrets.toml bestaat al"
}

Write-Host "`n[setup] Klaar."
if ($Start) {
  if (-not (Test-Path $App)) {
    Write-Warning "Bestand $App niet gevonden in $root"
  } else {
    Write-Host "[setup] Start app: $App"
    streamlit run $App
  }
} else {
  Write-Host "Start de app met:  venv\Scripts\activate ; streamlit run $App"
}

Write-Host "(Tip: als het script blokkades geeft, voer eenmalig uit: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned)"
