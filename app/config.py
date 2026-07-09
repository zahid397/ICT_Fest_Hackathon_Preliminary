"""Application configuration.

Values are read from environment variables so the same
image can run in different deployments.
"""

import os


JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "cowork-dev-secret-change-me"
)

JWT_ALGORITHM = "HS256"


# JWT requirements:
# Access token lifetime = exactly 900 seconds
ACCESS_TOKEN_EXPIRE_SECONDS = 900


# Refresh token lifetime = 7 days
REFRESH_TOKEN_EXPIRE_SECONDS = (
    7 * 24 * 60 * 60
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./cowork.db"
)
