from api.open_position.controller import router as open_position_router


def include_routers(app):
    app.include_router(open_position_router, prefix="/api", tags=["open_position"])
