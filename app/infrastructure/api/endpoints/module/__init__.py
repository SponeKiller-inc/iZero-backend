import pkgutil
import importlib
from pathlib import Path
from fastapi import APIRouter

router = APIRouter(prefix="/module", tags=["module"])

package_dir = Path(__file__).parent

# Dynamically importing and including all router in module folder
for module_info in pkgutil.iter_modules([str(package_dir)]):
    module = importlib.import_module(f"{__package__}.{module_info.name}")
    module_router = getattr(module, "router", None)
    if isinstance(module_router, APIRouter):
        router.include_router(module_router)
