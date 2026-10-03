import importlib
import pkgutil
from pathlib import Path

from fastapi import APIRouter


def build_aggregate_router(
    package_file: str,
    package_name: str,
    prefix: str,
    tags: list[str],
) -> APIRouter:
    """
    Builds an APIRouter that aggregates every `router` found in the sibling
    modules of the calling endpoint package (e.g. app/infrastructure/api/endpoints/<entity>).

    Args:
        package_file: The `__file__` of the calling package's __init__.py.
        package_name: The `__package__` of the calling package's __init__.py.
        prefix: URL prefix shared by all aggregated routers.
        tags: OpenAPI tags shared by all aggregated routers.

    Returns:
        The aggregate APIRouter with all discovered sub-routers included.
    """
    router = APIRouter(prefix=prefix, tags=tags)

    package_dir = Path(package_file).parent
    for module_info in pkgutil.iter_modules([str(package_dir)]):
        module = importlib.import_module(f"{package_name}.{module_info.name}")
        module_router = getattr(module, "router", None)
        if isinstance(module_router, APIRouter):
            router.include_router(module_router)

    return router
