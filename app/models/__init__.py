import pkgutil
import importlib
from pathlib import Path

package_dir = Path(__file__).parent

prefix = f"{__package__}."

for module_info in pkgutil.walk_packages(path=[str(package_dir)], prefix=prefix):
    importlib.import_module(module_info.name)