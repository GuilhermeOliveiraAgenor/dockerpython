import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+mysqlconnector://root:guizinho004@mysql:3306/apiproduct"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
