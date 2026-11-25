FROM nginx:alpine

# Install openssl for generating self-signed certificates
RUN apk add --no-cache openssl bash

# Create directories
RUN mkdir -p /etc/nginx/ssl /tmp/ssl

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy setup script
COPY setup-certs.sh /tmp/setup-certs.sh
RUN chmod +x /tmp/setup-certs.sh

# Copy ssl directory (may be empty or contain mkcert certs)
COPY --chown=root:root ssl /tmp/ssl

# Run certificate setup (either use mkcert certs or generate self-signed)
RUN /tmp/setup-certs.sh

EXPOSE 2316 2317

CMD ["nginx", "-g", "daemon off;"]
