import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(os.path.dirname(BASE_DIR), "instance")


class Config:
    """Application settings for local development and Render."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)

    # Render provides a PostgreSQL connection string through DATABASE_URL. Keep
    # SQLite as the no-setup local-development default.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(INSTANCE_DIR, 'inventory.db')}"
    ).replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
