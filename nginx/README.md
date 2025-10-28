# Nginx Reverse Proxy Setup

This configuration provides both HTTPS (default) and HTTP options for your Geneweb Docker services using Nginx as a reverse proxy.

## 🔒 Features

- **HTTPS encryption** for ports 2316 and 2317 (default)
- **HTTP option** available via `http` profile (no encryption)
- **Self-signed certificates** for development (generated automatically)
- **Trusted certificates** option using mkcert (no browser warnings!)
- **Automatic fallback** to self-signed if mkcert certs not available

## � Quick Reference

| Profile | Command | Ports | Protocol | Notes |
|---------|---------|-------|----------|-------|
| **HTTPS (prod)** | `docker compose --profile prod up -d` | 2316, 2317 | HTTPS | ⚠️ Self-signed cert warning |
| **HTTPS (ephemeral)** | `docker compose --profile ephemeral up -d` | 2316, 2317 | HTTPS | ⚠️ Self-signed cert warning |
| **HTTP (prod)** | `docker compose --profile http --profile prod up -d` | 2316, 2317 | HTTP | ✅ No warnings, no encryption |
| **HTTP (ephemeral)** | `docker compose --profile http --profile ephemeral up -d` | 2316, 2317 | HTTP | ✅ No warnings, no encryption |

## �🚀 Quick Start

### Option 1: HTTPS (Default - Recommended)

Start services with HTTPS (self-signed certificates):

```bash
# Production profile with HTTPS
docker compose --profile prod up -d

# Ephemeral profile with HTTPS
docker compose --profile ephemeral up -d
```

Access your services:
- **Port 2316:** https://localhost:2316
- **Port 2317:** https://localhost:2317

⚠️ **Browser Warning:** You'll see an "unsafe" warning because the certificate is self-signed. Click "Advanced" → "Proceed to localhost".

### Option 2: HTTP (No Encryption)

Start services with HTTP only (no SSL warnings, but no encryption):

```bash
# HTTP profile
docker compose --profile http up -d
```

Access your services:
- **Port 2316:** http://localhost:2316
- **Port 2317:** http://localhost:2317

✅ **No browser warnings!** But traffic is not encrypted.

**Note:** You need to also start your application services. Combine profiles:

```bash
# HTTP with prod services
docker compose --profile http --profile prod up -d

# HTTP with ephemeral services
docker compose --profile http --profile ephemeral up -d
```

## ✅ Remove Browser Warnings (Recommended for HTTPS)

To use **locally-trusted certificates** that won't show warnings:

### Windows (PowerShell)

```powershell
cd nginx
.\setup-trusted-certs.ps1
```

### Linux/Mac (Bash)

```bash
cd nginx
chmod +x setup-trusted-certs.sh
./setup-trusted-certs.sh
```

This will:
1. Install mkcert (if not already installed - follow the prompts)
2. Generate locally-trusted certificates
3. Place them in `nginx/ssl/`

Then rebuild and restart:

```bash
docker compose --profile prod build nginx
docker compose --profile prod up -d
```

🎉 **No more browser warnings!**

## 📦 Installing mkcert

If the setup script says mkcert is not installed:

### Windows
```powershell
# Using Chocolatey
choco install mkcert

# Using Scoop
scoop bucket add extras
scoop install mkcert
```

### macOS
```bash
brew install mkcert
```

### Linux (Ubuntu/Debian)
```bash
sudo apt install libnss3-tools
brew install mkcert  # Or download binary from GitHub
```

Download from: https://github.com/FiloSottile/mkcert/releases

## 🔐 Production: Using Real Certificates

For production, replace self-signed certificates with real ones (Let's Encrypt, etc.):

### Option A: Mount existing certificates

```yaml
nginx:
  volumes:
    - /path/to/cert.pem:/etc/nginx/ssl/cert.pem:ro
    - /path/to/key.pem:/etc/nginx/ssl/key.pem:ro
```

### Option B: Use Let's Encrypt with Certbot

1. Install certbot on your host
2. Generate certificates:
   ```bash
   certbot certonly --standalone -d yourdomain.com
   ```
3. Mount certificates in docker-compose.yml:
   ```yaml
   volumes:
     - /etc/letsencrypt/live/yourdomain.com/fullchain.pem:/etc/nginx/ssl/cert.pem:ro
     - /etc/letsencrypt/live/yourdomain.com/privkey.pem:/etc/nginx/ssl/key.pem:ro
   ```

### Option C: Use Traefik with automatic Let's Encrypt

See the `traefik/` directory for an alternative setup with automatic certificate management.

## 🛠️ Configuration

### Change domain names

Edit `nginx/nginx.conf` and update the `server_name` directives:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;  # Change this
    # ...
}
```

### Disable HTTPS (use HTTP only)

Remove the nginx service from docker-compose.yml and access services directly:
- Backoffice: http://localhost:5173
- Frontend: http://localhost:5174
- Backend: http://localhost:2316

### Custom SSL settings

Edit `nginx/nginx.conf` to modify:
- SSL protocols: `ssl_protocols TLSv1.2 TLSv1.3;`
- SSL ciphers: `ssl_ciphers '...';`
- Certificate paths

## 🐛 Troubleshooting

### "Connection refused" error
- Ensure all services are running: `docker-compose ps`
- Check nginx logs: `docker-compose logs nginx`

### "Certificate invalid" error
- This is expected with self-signed certificates in development
- For production, use real certificates (see above)

### Services not accessible
- Check hosts file is correctly configured
- Verify ports 80 and 443 are not used by other applications
- On Windows, ensure hosts file has no BOM (use Notepad++, save as UTF-8 without BOM)

### WebSocket connection failed
- Nginx is configured with WebSocket support for hot-reload
- If issues persist, check browser console for specific errors

## 📝 Notes

- The nginx service is included in both `prod` and `ephemeral` profiles
- Certificates are regenerated each time the nginx image is rebuilt
- For persistent certificates in development, mount a volume:
  ```yaml
  volumes:
    - ./nginx/ssl:/etc/nginx/ssl
  ```
