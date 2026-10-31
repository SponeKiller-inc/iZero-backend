# (calling code without "+" or "00", ISO 3166-1 alpha-3 country code) – only Czech phone
# numbers are supported for now
PHONE_PREFIXES: tuple[tuple[str, str], ...] = (
    ("420", "CZE"),
)
