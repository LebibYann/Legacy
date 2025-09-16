# Security & Hardening Guide

Practical steps to reduce risk when deploying GeneWeb (`gwd`) in production.

## 1. Authentication & Roles

| Role | Capabilities | Notes |
|------|--------------|-------|
| Public | View allowed data (subject to privacy rules) | Censored if young / restricted. |
| Friend | Expanded viewing (may bypass some censorship) | No structural edits. |
| Wizard | Full administrative powers (edit, import, setup) | Protect strongly. |

Recommendations:
- Use long, random passwords (at least 20 chars) for wizard/friend.
- Prefer HTTP Digest (`-auth_digest`) behind TLS; Basic only inside trusted TLS termination.

## 2. Limit Attack Surface

| Measure | Command / Config | Effect |
|---------|------------------|--------|
| Restrict client IPs | `-only_addr 192.168.1.0/24` (repeatable) | Blocks other networks. |
| Hide setup wizard | Omit `-setup_link` in production | Prevents web-based exec of maintenance tasks. |
| Disable unused plugins | Remove `-plugin` flags | Shrinks code surface. |
| Enforce deterministic tests only in dev | Avoid `-predictable` in prod | Keeps nonces unpredictable. |

## 3. TLS / Reverse Proxy

Run `gwd` behind Nginx/Apache/Caddy handling HTTPS + compression + rate limiting.

Example Nginx snippet:
```
location /geneweb/ {
  proxy_pass http://127.0.0.1:2317/;
  proxy_set_header Host $host;
  proxy_set_header X-Forwarded-Proto https;
  proxy_read_timeout 120s;
}
```
Use a distinct `-gw_prefix /geneweb` if path-based proxying.

## 4. Plugin Safety

- Only deploy plugins with verified sources; integrity is guarded by MD5 list unless overridden with `-unsafe_plugin` (avoid in prod).
- Keep plugin assets read-only to service user.
- Review plugin lexicon additions for script injection vectors.

## 5. Content Sanitization

- Maintain a curated allowed tags file via `-allowed_tags <file>`; keep minimal.
- Run `gwfixbase -invalid-utf8` after large imports to prevent malformed sequences that could trigger rendering quirks.

## 6. Least Privilege & Filesystem

| Item | Recommendation |
|------|---------------|
| Service User | Run under dedicated non-root user (e.g., `geneweb`). |
| Directory Permissions | Limit write to `<base>.gwb/` and logs; make binaries read-only. |
| Backups | Snapshot entire `<base>.gwb` directory (tar/rsync) while server quiescent. |
| Secrets | Restrict `cnt/gwd_private.txt` mode to 600. |

## 7. Logging & Monitoring

- Enable logging (`-log file`) and centralize (e.g., systemd journal forward).
- Monitor failed password attempts; enable `-trace_failed_passwd` temporarily when investigating.
- Track unusual surges in requests to `robots.txt` or repeated page patterns (bot indicators).

## 8. Privacy & Censorship

- Use `-c <years>` in export utilities (`gwexport`, etc.) before publishing shared dumps.
- Regularly audit censored vs visible persons (spot-check random samples).

## 9. Operational Playbooks

| Scenario | Action Steps |
|----------|--------------|
| Password compromise | Revoke by editing `.auth`; delete `cnt/gwd_private.txt`; restart; notify users. |
| Suspected plugin exploit | Remove plugin directory, restart with clean MD5 list, restore from backup if required. |
| Data corruption detected | Stop server, backup snapshot, run `gwfixbase -dry-run`, restore from last good backup if unrepairable. |

## 10. Rate Limiting (Proxy)

Implement basic rate limiting at proxy layer to deter brute force:
```
limit_req_zone $binary_remote_addr zone=gw:10m rate=30r/m;
location /geneweb/ {
  limit_req zone=gw burst=20 nodelay;
  ...
}
```

## 11. Future Hardening Ideas

| Idea | Benefit |
|------|---------|
| Argon2 hashed passwords | Stronger resistance vs offline attacks. |
| CSP headers from proxy | Mitigate XSS risk. |
| Session cookie JWT | Move auth off Basic/Digest (modernization). |
| Security audit script | Automated checklist run at CI. |

## 12. Checklist (Deploy)

- [ ] Reverse proxy with valid TLS cert
- [ ] No `-setup_link`
- [ ] Digest auth enabled
- [ ] Minimal plugins, all trusted
- [ ] Allowed tags file reviewed
- [ ] Service user non-root
- [ ] Backup schedule documented
- [ ] Monitoring alerts configured

See also: `binaries/gwd.md`, `operations/maintenance.md` (if created later).
