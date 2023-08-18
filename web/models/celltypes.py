"""Module to access, validate, and correct cell types."""
from levenshtein_finder import LevenshteinFinder

from models.exceptions import (
    CellTypeNotFoundError,
)


def get_celltype_index(celltype, celltypes, max_distance=3):
    """Get cell type index and correct cell type name if requested."""
    celltypes = list(celltypes)

    if celltype in celltypes:
        result = {
            'index': celltypes.index(celltype),
            'celltype': celltype,
        }
        return result

    if max_distance < 1:
        raise CellTypeNotFoundError(f"No cell type called {celltype} found.")

    # Autocorrection
    finder = LevenshteinFinder()
    finder.indexing(celltypes)
    # NOTE: this list is longer then one only for ties, in which case the first should be fine
    celltypes_close = finder.search(celltype, max_distance=max_distance)
    if len(celltypes_close) == 0:
        raise CellTypeNotFoundError(f"No cell type called {celltype} found.")

    result = {
        'index': celltypes_close[0]['idx'],
        'celltype': celltypes_close[0]['data'],
    }
    return result

