# PowerShell script to generate locally-trusted SSL certificates using mkcert
# This removes the "unsafe" warning in browsers for local development

Write-Host "=== Setting up locally-trusted SSL certificates ===" -ForegroundColor Green

# Check if mkcert is installed
$mkcertPath = Get-Command mkcert -ErrorAction SilentlyContinue

if (-not $mkcertPath) {
    Write-Host "`n❌ mkcert is not installed!" -ForegroundColor Red
    Write-Host "`nTo install mkcert on Windows:" -ForegroundColor Yellow
    Write-Host "1. Using Chocolatey: choco install mkcert" -ForegroundColor Cyan
    Write-Host "2. Using Scoop: scoop bucket add extras && scoop install mkcert" -ForegroundColor Cyan
    Write-Host "3. Download from: https://github.com/FiloSottile/mkcert/releases`n" -ForegroundColor Cyan
    exit 1
}

Write-Host "✅ mkcert found at: $($mkcertPath.Source)" -ForegroundColor Green

# Create ssl directory if it doesn't exist
$sslDir = "$PSScriptRoot\ssl"
if (-not (Test-Path $sslDir)) {
    New-Item -ItemType Directory -Path $sslDir | Out-Null
    Write-Host "✅ Created ssl directory: $sslDir" -ForegroundColor Green
}

# Install local CA (if not already done)
Write-Host "`nInstalling local Certificate Authority..." -ForegroundColor Yellow
mkcert -install

# Generate certificates for localhost
Write-Host "`nGenerating certificates for localhost..." -ForegroundColor Yellow
Set-Location $sslDir

mkcert -key-file key.pem -cert-file cert.pem localhost 127.0.0.1 ::1 "*.localhost"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Certificates generated successfully!" -ForegroundColor Green
    Write-Host "`nGenerated files:" -ForegroundColor Cyan
    Write-Host "  - $sslDir\cert.pem" -ForegroundColor White
    Write-Host "  - $sslDir\key.pem" -ForegroundColor White

    Write-Host "`n📝 Next steps:" -ForegroundColor Yellow
    Write-Host "1. Rebuild your Docker containers:" -ForegroundColor White
    Write-Host "   docker compose --profile prod build nginx" -ForegroundColor Cyan
    Write-Host "`n2. Start the services:" -ForegroundColor White
    Write-Host "   docker compose --profile prod up -d" -ForegroundColor Cyan
    Write-Host "`n3. Access your services without warnings:" -ForegroundColor White
    Write-Host "   https://localhost:2316" -ForegroundColor Cyan
    Write-Host "   https://localhost:2317" -ForegroundColor Cyan
    Write-Host "`n🎉 No more browser warnings!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Failed to generate certificates" -ForegroundColor Red
    exit 1
}
