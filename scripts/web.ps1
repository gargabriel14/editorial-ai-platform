param(
    [ValidateSet("start", "stop", "restart", "status", "open")]
    [string] $Action = "start",
    [int] $Port = 8765,
    [string] $HostAddress = "0.0.0.0"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$PidFile = Join-Path $RepoRoot "outputs\web-server.pid"
$OutLog = Join-Path $RepoRoot "outputs\web-server.out.log"
$ErrLog = Join-Path $RepoRoot "outputs\web-server.err.log"

New-Item -ItemType Directory -Force -Path (Join-Path $RepoRoot "outputs") | Out-Null

function Get-ListeningPid {
    $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($connection) {
        return $connection.OwningProcess
    }
    return $null
}

function Stop-WebServer {
    $pidToStop = $null
    if (Test-Path -LiteralPath $PidFile) {
        $pidToStop = [int](Get-Content -LiteralPath $PidFile -Raw)
    }
    if (-not $pidToStop) {
        $pidToStop = Get-ListeningPid
    }
    if ($pidToStop) {
        Stop-Process -Id $pidToStop -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
    }
    $listenerPid = Get-ListeningPid
    if ($listenerPid) {
        Stop-Process -Id $listenerPid -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
    }
    Remove-Item -LiteralPath $PidFile -Force -ErrorAction SilentlyContinue
}

function Start-WebServer {
    $existing = Get-ListeningPid
    if ($existing) {
        Write-Host "Port $Port is already listening with PID $existing"
        return
    }

    $srcPath = Join-Path $RepoRoot "src"
    $command = "`$env:PYTHONPATH='$srcPath'; python -m editorial_ai.cli --db data/editorial_ai.sqlite serve-web --host $HostAddress --port $Port"
    $proc = Start-Process -FilePath "powershell.exe" `
        -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", $command) `
        -WorkingDirectory $RepoRoot `
        -WindowStyle Hidden `
        -RedirectStandardOutput $OutLog `
        -RedirectStandardError $ErrLog `
        -PassThru
    Start-Sleep -Seconds 2
    $listenerPid = Get-ListeningPid
    if ($listenerPid) {
        Set-Content -LiteralPath $PidFile -Value $listenerPid -Encoding ASCII
    } else {
        Set-Content -LiteralPath $PidFile -Value $proc.Id -Encoding ASCII
    }
    Write-Host "Editorial AI dashboard: http://127.0.0.1:$Port"
    Write-Host "Docker/n8n endpoint: http://host.docker.internal:$Port"
}

switch ($Action) {
    "start" {
        Start-WebServer
    }
    "stop" {
        Stop-WebServer
    }
    "restart" {
        Stop-WebServer
        Start-WebServer
    }
    "status" {
        $listeningPid = Get-ListeningPid
        if ($listeningPid) {
            Write-Host "Listening on port $Port with PID $listeningPid"
        } else {
            Write-Host "Not listening on port $Port"
        }
    }
    "open" {
        Start-Process "http://127.0.0.1:$Port"
    }
}
