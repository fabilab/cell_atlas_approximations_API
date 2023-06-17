# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from config import configuration as config
from models import (
    get_highest_measurement,
    OrganismNotFoundError,
    FeatureNotFoundError,
)


class HighestMeasurement(Resource):
    """Get measurement in highest cell types"""

    def get(self):
        """Get expression in highest cell types, in one organism"""
        args = request.args
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        feature = args.get("feature", None)
        if feature is None:
            abort(400, message='The "feature" parameter is required.')
        unit = config["units"]["gene_expression"]
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
            result = get_highest_measurement(
                organism=organism,
                feature=feature,
                number=number,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except FeatureNotFoundError:
            abort(400, message="Some features could not be found.")

        return {
            "organism": organism,
            "feature": feature,
            "organs": result["organs"],
            "celltypes": result["celltypes"],
            "average": result["average"].tolist(),
            "unit": unit,
        }
