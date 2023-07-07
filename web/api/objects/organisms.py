# Web imports
from flask import request
from flask_restful import Resource

# Helper functions
from models import (
    get_organisms,
    MeasurementTypeNotFoundError,
)


class Organisms(Resource):
    """Get list of organisms"""

    def get(self):
        """Get list of organisms"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")

        try:
            organisms = get_organisms(
                measurement_type=measurement_type,
            )
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )


        return {
            "organisms": organisms,
            "measurement_type": measurement_type,
        }
