# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_feature_names,
    OrganismNotFoundError,
    MeasurementTypeNotFoundError,
)


class Features(Resource):
    """Get list of features for an organism"""

    def get(self):
        """Get list of features (genes)"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')

        try:
            features = get_feature_names(
                organism=organism,
                measurement_type=measurement_type,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "features": list(features),
        }
