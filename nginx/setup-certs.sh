#!/bin/bash
set -e

# Check if mkcert certificates exist in /tmp/ssl
if [ -f /tmp/ssl/cert.pem ] && [ -f /tmp/ssl/key.pem ]; then
    echo "✅ Using mkcert certificates (no browser warnings)"
    cp /tmp/ssl/cert.pem /etc/nginx/ssl/cert.pem
    cp /tmp/ssl/key.pem /etc/nginx/ssl/key.pem
else
    echo "⚠️  Generating self-signed certificates (browser will show warning)"
    echo "    To remove warnings, run: ./setup-trusted-certs.ps1 (Windows) or ./setup-trusted-certs.sh (Linux/Mac)"
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/key.pem \
        -out /etc/nginx/ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
        -addext "subjectAltName=DNS:localhost,DNS:*.localhost,IP:127.0.0.1"
fi

# Verify certificates exist
if [ ! -f /etc/nginx/ssl/cert.pem ] || [ ! -f /etc/nginx/ssl/key.pem ]; then
    echo "❌ Failed to setup SSL certificates"
    exit 1
fi

echo "✅ SSL certificates ready"
