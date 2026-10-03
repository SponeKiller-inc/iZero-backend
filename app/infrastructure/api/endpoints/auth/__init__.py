from app.infrastructure.api.endpoints._router_loader import build_aggregate_router

router = build_aggregate_router(__file__, __package__, prefix="/auth", tags=["auth"])
