# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_organs,
    get_celltypes,
    OrganismNotFoundError,
    OrganNotFoundError,
    MeasurementTypeNotFoundError,
)
from api.v1.utils import clean_organ_string


class Celltypes(Resource):
    """Get list of cell types for an organ and organism"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        organ = args.get("organ", None)
        if organ is None:
            abort(400, message='The "organ" parameter is required.')
        organ = clean_organ_string(organ)
        measurement_type = args.get(
            "measurement_type", "gene_expression")

        try:
            celltypes = list(get_celltypes(organism=organism, organ=organ))
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except OrganNotFoundError:
            abort(400, message=f"Organ not found: {organ}.")
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )

        return {
            "organism": organism,
            "organ": organ,
            "measurement_type": measurement_type,
            "celltypes": celltypes,
        }
