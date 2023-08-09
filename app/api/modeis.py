from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pymongo import MongoClient

from app.config import settings
from app.db import ActiveMongo
from app.template import templates
from app.utils.gee import getMODIS_Series

router = APIRouter()


@router.get('json/{lon}/{lat}')
def ndvi_data(*, db: MongoClient = ActiveMongo, lon: float, lat: float):
    series = db.evi_ndvi.find_one({'lon': lon, 'lat': lat})
    if series is not None:
        return series['data']
    else:
        _data = getMODIS_Series(lon, lat)
        db.evi_ndvi.insert_one({'lon': lon, 'lat': lat, 'data': _data})
        return _data


@router.get('chart/{lon}/{lat}', response_class=HTMLResponse)
def ndvi_chart(request: Request, lon: float, lat: float):
    return templates.TemplateResponse(
        'ndvi.html',
        {
            'request': request,
            'lon': lon,
            'lat': lat,
            'server_url': settings.SERVER_URL,
        },
    )
