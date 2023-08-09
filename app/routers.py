from app.api import modeis, analytics


def created_routes(app):

    app.include_router(modeis.router, prefix='/api/modis', tags=['modis'])
    app.include_router(analytics.router, prefix='/api/analytics', tags=['analytics'])

    return app
