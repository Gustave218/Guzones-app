import os
class Config:
    SECRET_KEY = "guzones-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
