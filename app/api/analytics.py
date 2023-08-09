
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
import io

from app.config import settings, logger
from app.db import ActiveMongo
from app.models.tvi import ServerTVI
from fastapi.responses import StreamingResponse

import geopandas as gpd
import pandas as pd


router = APIRouter()

def to_dataFrame(points_db,campaign_db,campaign_id):
    campaign = campaign_db.find_one({'_id':campaign_id},{'numInspec':1,'initialYear':1,'finalYear':1})
    
    nInspections = int(campaign['numInspec'])
    initialYear = int(campaign['initialYear'])
    finalYear = int(campaign['finalYear'])

    colNames = ["id","lat","lon"]
    
    for i in range(1, nInspections+1):
        colNames.append(f'user_{i}' )
        colNames.append(f'time_{i}')
        for y in range(initialYear,finalYear+1):
            colNames.append(f'class_{y}_{i}')
            colNames.append(f'border_{y}_{i}')
            
    for y in range(initialYear,finalYear+1):
        colNames.append(f'class_{y}_f')
        
    for y in range(initialYear,finalYear+1):
        colNames.append(f'border_{y}_f')
        colNames.append(f'score_{y}_f')

    for point in points_db.find({ 'campaign':campaign_id }):
        check = {}

        if len(point['inspection']) >= nInspections:
            result = [ point['_id'], point['lon'], point['lat']]
            for i in range(0 ,nInspections):

                inspection = point['inspection'][i]
                if (point['userName'][i]):
                    result.append(point['userName'][i].upper())
                    result.append(inspection['counter'])
                    for form in inspection['form']:
                        
                        
                        for y in range(form['initialYear'], form['finalYear']+1): 
                            landUse = form['landUse']
                            result.append(form['landUse'])
                            try:
                                pixelBorder = form['pixelBorder']
                            except:
                                pixelBorder = False
                            
                            
                            result.append(pixelBorder)
                            
                            try:
                                check[y]['border'].append(pixelBorder)
                                check[y]['landUse'].append(landUse)
                            except:
                                check[y] = {}
                                check[y]['border'] = []
                                check[y]['landUse'] = []
                                check[y]['border'].append(pixelBorder)
                                check[y]['landUse'].append(landUse)
                                
            try:
                consolidateds = point['classConsolidated'] 
                if consolidateds:
                    for y, consolidated in enumerate(consolidateds, initialYear):
                        score = check[y]['landUse'].count(consolidated)
                        check[y]['score'] = score if score > 0 else 1
                        check[y]['consolidated'] = consolidated
                        check[y]['border'] = any(check[y]['border'])
                        result.append(consolidated)

                for i in check:
                    result.append(check[i]['border'])
                    result.append(check[i]['score'])
            except KeyError:
                logger.error('Error not found consolidated')
                HTTPException(status_code=409, detail=f"There are still unresolved issues for the campaign/login {campaign_id}. Therefore, it is not possible to generate the final report")
                

            yield dict(zip(colNames,result))
        else:
            logger.error('Error not found inspection')
            HTTPException(status_code=409, detail="It will only be possible to generate the Inspection Report after the completion of all inspections of all points of the campaign/login.")


@router.get('/{server_name}/{campaign_id}/{filetype}', response_class=StreamingResponse)
async def get_resumo(
    *,
    server_name:ServerTVI, 
    campaign_id: str,
    filetype:str, 
    db: MongoClient = ActiveMongo,
    direct: bool = Query(True, description="Download the file directly")):
    logger.debug(server_name,campaign_id)
    points_db = db[server_name].points
    campaign_db = db[server_name].campaign
    try:
        df = pd.DataFrame(to_dataFrame(points_db,campaign_db,campaign_id))
        
        stream = io.StringIO()
        
        
        match filetype:
            case 'csv':
                df.to_csv(stream, index=False)
                response = StreamingResponse(
                    iter([stream.getvalue()]), media_type="text/csv")
                if direct:
                    response.headers["Content-Disposition"] = f"attachment; filename={server_name}_{campaign_id}.csv"
                return response
            case 'geojson':
                gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")
                stream.write(gdf.to_json())
                response = StreamingResponse(
                    iter([stream.getvalue()]), media_type="application/geo+json")
                if direct:
                    response.headers["Content-Disposition"] = f"attachment; filename={server_name}_{campaign_id}.geojson"
                return response
            case _:
                HTTPException(status_code=404, detail="Item not found")
        
    except:
        logger.exception('Error')
        HTTPException(status_code=404, detail="Item not found")
        
        
        
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import StreamingResponse


app = FastAPI()


@app.get("/data/", response_class=StreamingResponse)
async def export_data():
    # Create a sample dataframe
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(
        iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response



