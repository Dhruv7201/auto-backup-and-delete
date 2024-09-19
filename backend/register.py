from views.index import router as index_router


def register_routes(app):
    app.include_router(index_router)