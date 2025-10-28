#!/bin/bash
# Bash script to generate locally-trusted SSL certificates using mkcert
# This removes the "unsafe" warning in browsers for local development

set -e

echo "=== Setting up locally-trusted SSL certificates ==="

# Check if mkcert is installed
if ! command -v mkcert &> /dev/null; then
    echo ""
    echo "❌ mkcert is not installed!"
    echo ""
    echo "To install mkcert:"
    echo "  Ubuntu/Debian: sudo apt install libnss3-tools && brew install mkcert"
    echo "  macOS: brew install mkcert"
    echo "  Or download from: https://github.com/FiloSottile/mkcert/releases"
    echo ""
    exit 1
fi

echo "✅ mkcert found at: $(which mkcert)"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SSL_DIR="$SCRIPT_DIR/ssl"

# Create ssl directory if it doesn't exist
if [ ! -d "$SSL_DIR" ]; then
    mkdir -p "$SSL_DIR"
    echo "✅ Created ssl directory: $SSL_DIR"
fi

# Install local CA (if not already done)
echo ""
echo "Installing local Certificate Authority..."
mkcert -install

# Generate certificates for localhost
echo ""
echo "Generating certificates for localhost..."
cd "$SSL_DIR"

mkcert -key-file key.pem -cert-file cert.pem localhost 127.0.0.1 ::1 "*.localhost"

echo ""
echo "✅ Certificates generated successfully!"
echo ""
echo "Generated files:"
echo "  - $SSL_DIR/cert.pem"
echo "  - $SSL_DIR/key.pem"
echo ""
echo "📝 Next steps:"
echo "1. Rebuild your Docker containers:"
echo "   docker compose --profile prod build nginx"
echo ""
echo "2. Start the services:"
echo "   docker compose --profile prod up -d"
echo ""
echo "3. Access your services without warnings:"
echo "   https://localhost:2316"
echo "   https://localhost:2317"
echo ""
echo "🎉 No more browser warnings!"
