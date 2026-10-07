from app.infrastructure.providers.http_audit import install_http_audit

# Installed as soon as this package (or any of its submodules, e.g.
# auth_google.py) is imported - guarantees the audit hook is in place before
# any provider makes its first real outbound HTTP call.
install_http_audit()
