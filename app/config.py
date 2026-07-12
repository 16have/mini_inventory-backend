import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(os.path.dirname(BASE_DIR), "instance")

class Config:
    SECRET_KEY = "178Inventory"
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(INSTANCE_DIR, 'inventory.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config:
    SECRET_KEY = "178Inventory"

    JWT_SECRET_KEY = "InventoryJWTSecret"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'inventory.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False