from json import load as jload
from pathlib import Path

import ee
from fastapi import FastAPI, status
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.oauth2 import service_account
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import logger, settings, start_logger
from app.middleware.TokenMiddleware import TokenMiddleware
from app.middleware.analytics import Analytics
from app.routers import created_routes

start_logger()

app = FastAPI()
app.add_middleware(TokenMiddleware)
app.add_middleware(Analytics, api_name=settings.API_NAME)

from app.utils.cors import origin_regex, allow_origins

# Configurações CORS com expressões regulares para subdomínios dinâmicos
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # Lista de origens estáticas (deixe vazio se estiver usando regex)
    allow_methods=["*"],  # Métodos permitidos
    allow_headers=["*"],  # Cabeçalhos permitidos
    allow_credentials=True,  # Permite o envio de cookies/credenciais
    allow_origin_regex=origin_regex,
    expose_headers=["X-Response-Time"],  # Cabeçalhos expostos
    max_age=3600,  # Tempo máximo para cache da resposta preflight
)

app = created_routes(app)

templates_path = Path('templates')
templates = Jinja2Templates(directory=templates_path)

app.mount('/static', StaticFiles(directory=templates_path.resolve()), 'static')


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    start_code = exc.status_code
    if request.url.path.split('/')[1] == 'api':
        return JSONResponse(
            content={'status_code': start_code, 'message': exc.detail},
            status_code=start_code,
            headers=exc.headers,
        )
    base_url = request.base_url
    if settings.HTTPS:
        base_url = f'{base_url}'.replace('http://', 'https://')
    return templates.TemplateResponse(
        'error.html',
        {
            'request': request,
            'base_url': base_url,
            'info': '',
            'status': start_code,
            'message': exc.detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors(), 'body': exc.body}),
        headers={
            'X-Download-Detail': f'{exc.errors()}',
            'X-Download-Body': f'{exc.body}',
        },
    )


@app.on_event('startup')
async def startup():
    logger.debug('startup')
    """
    Inicializa o Google Earth Engine usando um arquivo de chave privada de Service Account.

    Args:
        private_key_file (str): Caminho para o arquivo de chave privada (.json).
    """
    try:
        service_account_file = settings.PRIVATE_KEY_FILE
        logger.info(f"service_account_file: {service_account_file}")
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=["https://www.googleapis.com/auth/earthengine.readonly"],
        )
        ee.Initialize(credentials=credentials)

        logger.info("GEE Initialized successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to initialize GEE")


@app.on_event('shutdown')
async def shutdown():
    """Perform shutdown activities."""
    ee.Reset()
    pass


def custom_openapi():
    try:
        with open('/APP/version.json') as user_file:
            parsed_json = jload(user_file)
            version = parsed_json['commitId']
    except:
        version = 'not-informad'
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='Lapig - Laboratório de Processamento de Imagens e Geoprocessamento',
        version=version,
        contact={'name': 'Lapig', 'url': 'https://lapig.iesa.ufg.br/'},
        description='API de timeseries do Lapig',
        routes=app.routes,
    )
    openapi_schema['info']['x-logo'] = {
        'url': 'https://files.cercomp.ufg.br/weby/up/1313/o/Marca_Lapig_PNG_sem_descri%C3%A7%C3%A3o-removebg-preview.png?1626024108'
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
