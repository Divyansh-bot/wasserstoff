# Activate Python 3.10 virtual environment for DocuMind AI

$venvPath = "$PSScriptRoot\.venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    Write-Host "✅ Activating Python 3.10 environment..."
    & $venvPath
} else {
    Write-Host "⚠️ .venv not found. Creating virtual environment with Python 3.10..."

    $python310 = "C:\Users\divya\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\python3.10.exe"
    
    if (Test-Path $python310) {
        & $python310 -m venv "$PSScriptRoot\.venv"
        Write-Host "✅ Virtual environment created. Activating now..."
        & "$PSScriptRoot\.venv\Scripts\Activate.ps1"
    } else {
        Write-Host "❌ Python 3.10 executable not found at expected path."
    }
}
