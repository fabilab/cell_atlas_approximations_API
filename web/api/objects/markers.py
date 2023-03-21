# Web imports
from flask import request
from flask_restful import Resource

# Helper functions
from models import (
    get_markers,
)


class Markers(Resource):
    """Get average measurement by cell type"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism", None)
        organ = args.get("organ", None)
        cell_type = args.get("celltype", None)
        number = args.get("number", None)

        try:
            number = int(number)
        except (TypeError, ValueError):
            number = None

        if (
            (organism is None)
            or (organ is None)
            or (cell_type is None)
            or (number is None)
        ):
            markers = None
        else:
            try:
                markers = get_markers(
                    organism=organism,
                    organ=organ,
                    cell_type=cell_type,
                    number=number,
                )
            except KeyError:
                markers = None

        if markers is not None:
            return {
                "organism": organism,
                "organ": organ,
                "celltype": cell_type,
                "markers": list(markers),
            }

        # TODO
        return None
