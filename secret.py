import secrets
import string

# Define the length of the secret
secret_length = 32

# Generate a secure random secret (hexadecimal format)
secret = secrets.token_hex(secret_length)
print("Generated Secret (hex):", secret)
