"""Database connection"""
from fastapi import Depends
from sqlmodel import Session, create_engine

from .config import settings

engine = create_engine(
    settings.db.uri,
    echo=settings.db.echo,
    connect_args=settings.db.connect_args,
)


def get_session_postgis():
    with Session(engine) as session:
        yield session



def get_session_mongo():
    with MongoClient(settings.MONGODB_URL) as client:
        yield client


ActiveMongo = Depends(get_session_mongo)
ActivePostGis = Depends(get_session_postgis)