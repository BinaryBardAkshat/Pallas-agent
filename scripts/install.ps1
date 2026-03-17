# Pallas Agent — Windows Installer
# Usage: irm https://raw.githubusercontent.com/vinkura-ai/pallas/main/scripts/install.ps1 | iex

#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$PALLAS_VERSION  = "0.1.4"
$MIN_PYTHON_MAJ  = 3
$MIN_PYTHON_MIN  = 11

# ─── Helpers ──────────────────────────────────────────────────────────────────
function Write-Ok   ([string]$msg) { Write-Host "  [OK]  $msg" -ForegroundColor Green  }
function Write-Info ([string]$msg) { Write-Host "  -->   $msg" -ForegroundColor Cyan   }
function Write-Warn ([string]$msg) { Write-Host "  [!]   $msg" -ForegroundColor Yellow }
function Write-Fail ([string]$msg) {
    Write-Host "  [X]   $msg" -ForegroundColor Red
    exit 1
}
function Write-Step ([string]$msg) {
    Write-Host ""
    Write-Host $msg -ForegroundColor Cyan -NoNewline
    Write-Host ""
}

# ─── Banner ───────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "+---------------------------------+" -ForegroundColor Cyan
Write-Host "|    Pallas Agent Installer       |" -ForegroundColor Cyan
Write-Host "|        v$PALLAS_VERSION                 |" -ForegroundColor Cyan
Write-Host "+---------------------------------+" -ForegroundColor Cyan
Write-Host ""

# ─── Detect if running from a local repo checkout ────────────────────────────
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$InRepo      = $false
$ProjectRoot = ""
if ($ScriptDir -and (Test-Path (Join-Path $ScriptDir "..\pyproject.toml"))) {
    $ProjectRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path
    $InRepo = $true
}

# ─── Step 1: Check Python >= 3.11 ─────────────────────────────────────────────
Write-Step "Checking Python version..."

$PythonBin = $null
$Candidates = @("python", "python3", "python3.13", "python3.12", "python3.11")

foreach ($candidate in $Candidates) {
    $found = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($found) {
        try {
            $verStr = & $candidate -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
            $parts  = $verStr.Trim().Split('.')
            $maj    = [int]$parts[0]
            $min    = [int]$parts[1]
            if (($maj -gt $MIN_PYTHON_MAJ) -or ($maj -eq $MIN_PYTHON_MAJ -and $min -ge $MIN_PYTHON_MIN)) {
                $PythonBin = $candidate
                Write-Ok "Found $candidate ($verStr)"
                break
            }
        } catch { }
    }
}

if (-not $PythonBin) {
    Write-Host ""
    Write-Host "  Python 3.11+ is required but was not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "  Install Python using winget:" -ForegroundColor Yellow
    Write-Host "    winget install Python.Python.3.13" -ForegroundColor White
    Write-Host ""
    Write-Host "  Or download from: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host ""
    exit 1
}

# ─── Step 2: Check / Install uv ───────────────────────────────────────────────
Write-Step "Checking for uv package manager..."

$UvAvailable = $false
$uvCmd = Get-Command uv -ErrorAction SilentlyContinue

if ($uvCmd) {
    $uvVer = (& uv --version 2>&1) -replace "uv ", ""
    Write-Ok "uv $uvVer already installed"
    $UvAvailable = $true
} else {
    Write-Warn "uv not found — installing..."
    try {
        # Official uv Windows installer
        $uvInstallScript = (Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -UseBasicParsing).Content
        Invoke-Expression $uvInstallScript

        # Refresh PATH for this session
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + $env:PATH

        $uvCmd = Get-Command uv -ErrorAction SilentlyContinue
        if ($uvCmd) {
            Write-Ok "uv installed successfully"
            $UvAvailable = $true
        } else {
            Write-Warn "uv installed but not yet on PATH. Will fall back to pip."
        }
    } catch {
        Write-Warn "Could not install uv automatically: $_"
        Write-Warn "Falling back to pip."
    }
}

# ─── Step 3: Install Pallas ───────────────────────────────────────────────────
Write-Step "Installing Pallas Agent v${PALLAS_VERSION}..."

if (-not $UvAvailable) {
    Write-Info "Installing via pip (pallas-agent)..."
    & $PythonBin -m pip install --upgrade pallas-agent
    Write-Ok "Installed pallas-agent via pip"
} elseif ($InRepo) {
    Write-Info "Installing from local source: $ProjectRoot"
    # Idempotent: uninstall first, ignore errors
    & uv tool uninstall pallas-agent 2>$null
    Push-Location $ProjectRoot
    try {
        & uv tool install . --force
    } finally {
        Pop-Location
    }
    Write-Ok "Installed from local source"
} else {
    Write-Info "Installing pallas-agent from PyPI..."
    & uv tool uninstall pallas-agent 2>$null
    & uv tool install pallas-agent --force
    Write-Ok "Installed pallas-agent from PyPI"
}

# Ensure uv tool bin is on PATH
try {
    $uvToolBin = (& uv tool dir 2>$null).Trim() + "\bin"
    if (Test-Path $uvToolBin) {
        $env:PATH = "$uvToolBin;$env:PATH"
    }
} catch { }

# Also add %USERPROFILE%\.local\bin (pip scripts)
$localBin = Join-Path $env:USERPROFILE ".local\bin"
if (Test-Path $localBin) { $env:PATH = "$localBin;$env:PATH" }

# ─── Step 4: pallas doctor ────────────────────────────────────────────────────
Write-Step "Running pallas doctor..."

$pallasCmd = Get-Command pallas -ErrorAction SilentlyContinue
if ($pallasCmd) {
    & pallas doctor
    if ($LASTEXITCODE -ne 0) {
        Write-Warn "pallas doctor reported issues. Check your API key configuration."
    }
} else {
    Write-Warn "'pallas' command not found on PATH after install."
    Write-Warn "You may need to restart your terminal or add the uv tools bin to PATH:"
    Write-Warn "  `$env:PATH += `";`$env:USERPROFILE\.local\bin`""
    Write-Warn "Then run: pallas doctor"
}

# ─── Done ─────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "+----------------------------------------------+" -ForegroundColor Green
Write-Host "|  Pallas installed! Run: pallas start         |" -ForegroundColor Green
Write-Host "+----------------------------------------------+" -ForegroundColor Green
Write-Host ""
Write-Host "  Docs:    https://github.com/vinkura-ai/pallas" -ForegroundColor DarkGray
Write-Host "  Config:  $env:USERPROFILE\.pallas\config.json" -ForegroundColor DarkGray
Write-Host ""
