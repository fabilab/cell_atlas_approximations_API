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
        raise OrganismNotFoundError(
            f"Organism not found: {organism}",
            organism=organism,
        )
    return approx_path


def get_interactions_path(organism):
    """Get the file path for a set of interactions."""
    interaction_folder = pathlib.Path(config["paths"]["interactions"])
    filename = f"{organism}_omnipath_nocomplex_dedup.tsv.gz"
    interaction_path = interaction_folder / filename
    if not interaction_path.exists():
        raise OrganismNotFoundError(
            f"Organism not found: {organism}",
            organism=organism,
        )
    return interaction_path


def get_protein_embeddings_path():
    """Get the file containing all protein embeddings."""
    return pathlib.Path(config["paths"]["protein_embeddings"])
