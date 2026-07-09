param(
    [ValidateSet("start", "stop", "restart", "status", "logs", "pull", "import-workflow", "open")]
    [string] $Action = "start"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ComposeDir = Join-Path $RepoRoot "infra\n8n"
$ComposeFile = Join-Path $ComposeDir "docker-compose.yml"
$EnvFile = Join-Path $ComposeDir ".env"
$EnvExampleFile = Join-Path $ComposeDir ".env.example"

$DockerCommand = Get-Command docker -ErrorAction SilentlyContinue
if ($DockerCommand) {
    $Docker = $DockerCommand.Source
} else {
    $Docker = "C:\Program Files\Docker\Docker\resources\bin\docker.exe"
}

if (-not (Test-Path -LiteralPath $Docker)) {
    throw "Docker CLI not found. Install Docker Desktop or add docker.exe to PATH."
}

$DockerBinDir = Split-Path -Parent $Docker
if (($env:Path -split ";") -notcontains $DockerBinDir) {
    $env:Path = "$DockerBinDir;$env:Path"
}

function New-EncryptionKey {
    $bytes = New-Object byte[] 32
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try {
        $rng.GetBytes($bytes)
    } finally {
        $rng.Dispose()
    }
    return (($bytes | ForEach-Object { $_.ToString("x2") }) -join "")
}

function Ensure-EnvFile {
    if (Test-Path -LiteralPath $EnvFile) {
        return
    }

    $key = New-EncryptionKey
    $content = Get-Content -LiteralPath $EnvExampleFile -Raw
    $content = $content.Replace("N8N_ENCRYPTION_KEY=replace-with-a-generated-secret", "N8N_ENCRYPTION_KEY=$key")
    Set-Content -LiteralPath $EnvFile -Value $content -Encoding UTF8
    Write-Host "Created local env file: $EnvFile"
}

function Invoke-DockerCompose {
    & $Docker compose --project-name editorial-ai-n8n --env-file $EnvFile -f $ComposeFile @args
    if ($LASTEXITCODE -ne 0) {
        throw "docker compose failed with exit code $LASTEXITCODE"
    }
}

Ensure-EnvFile

switch ($Action) {
    "start" {
        Invoke-DockerCompose up -d
        Write-Host "n8n should be available at http://localhost:5678"
    }
    "stop" {
        Invoke-DockerCompose down
    }
    "restart" {
        Invoke-DockerCompose down
        Invoke-DockerCompose up -d
        Write-Host "n8n should be available at http://localhost:5678"
    }
    "status" {
        Invoke-DockerCompose ps
    }
    "logs" {
        Invoke-DockerCompose logs -f n8n
    }
    "pull" {
        Invoke-DockerCompose pull
    }
    "import-workflow" {
        Invoke-DockerCompose exec -T n8n n8n import:workflow --input=/home/node/editorial-workflows/opportunity_pipeline.workflow.json
    }
    "open" {
        Start-Process "http://localhost:5678"
    }
}
