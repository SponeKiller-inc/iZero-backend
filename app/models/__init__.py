import pkgutil
import importlib
from pathlib import Path

package_dir = Path(__file__).parent
for module in pkgutil.iter_modules([str(package_dir)]):
    importlib.import_module(f"{__package__}.{module.name}")