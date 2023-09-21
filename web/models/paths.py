import pathlib
from config import configuration as config
from models.exceptions import (
    OrganismNotFoundError,
)


def get_atlas_path(organism):
    """Get the file path for a compressed atlas."""
    atlas_folder = pathlib.Path(config["paths"]["compressed_atlas"])
    filename = organism + ".h5"
    approx_path = atlas_folder / filename
    if not approx_path.exists():
        raise OrganismNotFoundError(f"Organism not found: {organism}")
    return approx_path
