from datetime import date
from glob import glob
from random import randint

import ee

from app.config import settings


def gee_multi_credentials(credentials_dir):
    def mpb_get_credentials_path():
        credentials_files = ee.oauth.credentials_files

        credential = credentials_files[randint(0, 5)]
        ee.oauth.current_credentials_idx += 1

        return credential

    ee.oauth.current_credentials_idx = 0
    ee.oauth.credentials_files = glob(credentials_dir + '/*.json')

    ee.oauth.get_credentials_path = mpb_get_credentials_path


def getMODIS_Series(lon, lat):
    gee_multi_credentials(settings.GEE_CREDENCIALS_DIR)
    ee.Initialize()

    def mask_badPixels(img):
        mask = img.select('SummaryQA').eq(0)
        img = img.mask(mask)
        return img

    MODIS = (
        ee.ImageCollection('MODIS/006/MOD13Q1')
        .filterDate('2000', str(int(date.today().year) + 1))
        .map(mask_badPixels)
        .select('NDVI', 'EVI')
    )

    geo = ee.Geometry.Point([lon, lat])

    data = []

    pointSeries = MODIS.getRegion(
        geo, MODIS.first().projection().nominalScale()
    ).getInfo()

    for index, dt in enumerate(pointSeries):
        if index > 1 and dt[4] != None and dt[4] != None:
            _date = dt[0].split('_')
            data.append(
                {
                    'label': f'{_date[2]}/{_date[1]}/{_date[0]}',
                    'ndvi': dt[4] / 10000,
                    'evi': dt[5] / 10000,
                }
            )

    ee.Reset()
    return data
