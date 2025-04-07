"""Database connection"""
from fastapi import Depends
from pymongo import MongoClient

from .config import settings


def get_session_mongo():
    with MongoClient(settings.MONGO_URL) as client:
        yield client

ActiveMongo = Depends(get_session_mongo)
