# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_markers,
    OrganismNotFoundError,
    OrganNotFoundError,
    CellTypeNotFoundError,
)


class Markers(Resource):
    """Get average measurement by cell type"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        organ = args.get("organ", None)
        if organ is None:
            abort(400, message='The "organ" parameter is required.')
        cell_type = args.get("celltype", None)
        if cell_type is None:
            abort(400, message='The "celltype" parameter is required.')
        number = args.get("number", None)
        if number is None:
            abort(400, message='The "number" parameter is required.')

        try:
            number = int(number)
        except (TypeError, ValueError):
            abort(400, message='The "number" parameter should be an integer.')

        if number <= 0:
            abort(400, message='The "number" parameter should be positive.')

        try:
            markers = get_markers(
                organism=organism,
                organ=organ,
                cell_type=cell_type,
                number=number,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except OrganNotFoundError:
            abort(400, message=f"Organ not found: {organ}.")
        except CellTypeNotFoundError:
            abort(400, message=f"Cell type not found: {cell_type}.")

        return {
            "organism": organism,
            "organ": organ,
            "celltype": cell_type,
            "markers": list(markers),
        }
