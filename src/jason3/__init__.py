"""
Jason-3 Satellite Data Download Package.
"""
# Standard library imports
from importlib import resources

try:
    import tomllib
except ModuleNotFoundError:
    # Third party imports
    import tomli as tomllib


# Version of package
__version__ = "1.0.0"

# Read URL of the Real Python feed from config file
_cfg = tomllib.loads(resources.read_text("jason3", "config.toml"))
URL = _cfg["feed"]["url"]
