import os
class Config:
    SECRET_KEY = "guzones-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:////data/guzone.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

TEAM_EMAILS = os.getenv("TEAM_EMAILS", "").split(",")