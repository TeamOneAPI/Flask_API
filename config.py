import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///bluewave.db"  # US-19
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
