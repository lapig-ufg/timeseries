from .server import modeis


def created_routes(app):

    app.include_router(
        modeis.router, prefix='/api/modis', tags=['modis']
    )

    
    return app