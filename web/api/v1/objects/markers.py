# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_markers,
    OrganismNotFoundError,
    OrganNotFoundError,
    CellTypeNotFoundError,
    MeasurementTypeNotFoundError,
)
from api.v1.utils import clean_organ_string


class Markers(Resource):
    """Get average measurement by cell type"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        organ = args.get("organ", None)
        if organ is None:
            abort(400, message='The "organ" parameter is required.')
        organ = clean_organ_string(organ)
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
                measurement_type=measurement_type,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except OrganNotFoundError:
            abort(400, message=f"Organ not found: {organ}.")
        except CellTypeNotFoundError:
            abort(400, message=f"Cell type not found: {cell_type}.")
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )

        return {
            "organism": organism,
            "organ": organ,
            "measurement_type": measurement_type,
            "celltype": cell_type,
            "markers": list(markers),
        }
