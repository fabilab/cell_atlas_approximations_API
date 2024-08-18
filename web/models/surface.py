import h5py

from config import configuration as config

from models.exceptions import (
    OrganismNotFoundError,
)


def get_surface_genes(organism):
    """Get the genes that encode for cell surface proteins in an organism."""
    with h5py.File(config['paths']['surface_genes']) as h5:
        if organism not in h5:
            raise OrganismNotFoundError(
                f"Surface genes not available for organism: {organism}",
                organism=organism,
            )
        genes = h5[organism].asstr()[:]
    return genes
