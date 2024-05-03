
import secrets

class Config:
    # Generate a random secret key
    SECRET_KEY = secrets.token_hex(16)


