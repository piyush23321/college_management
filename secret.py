import secrets


# Generate a secure 256-bit secret key (HMAC token)
hmac_secret = secrets.token_hex(32)
print(f"Generated HMAC Secret: {hmac_secret}")
