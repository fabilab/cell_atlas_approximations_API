import os
import pathlib

from models.utils import ApproximationFile


# Global lists of organisms, evaluated lazily
organisms = {}

def load_organisms(
    measurement_type="gene_expression",
):
    """Load a list of organisms and store it in memory."""
    atlas_folder = pathlib.Path(config["paths"]["compressed_atlas"])
    _organisms = []
    for filename in os.listdir(atlas_folder):
        organism, ending = filename.split(".")[0]
        if ending != "h5":
            continue
        approx_path = atlas_folder / filename
        with ApproximationFile(approx_path) as db:
            if measurement_type in db:
                _organisms.append(organism)
    _organisms.sort()
    organisms[measurement_type] = _organisms


def get_organisms(
    measurement_type="gene_expression",
):
    """Get a list of organisms supported, for a particular measurement type."""
    if measurement_type not in organisms:
        load_organisms(measurement_type)
    return organisms[measurement_type]

