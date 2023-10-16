# Web imports
from flask import request
from flask_restful import Resource

# Helper functions
from models import (
    get_organisms,
)
from api.v1.exceptions import (
    model_exceptions,
)


class Organisms(Resource):
    """Get list of organisms"""

    @model_exceptions
    def get(self):
        """Get list of organisms"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")

        organisms = get_organisms(
            measurement_type=measurement_type,
        )

        return {
            "organisms": organisms,
            "measurement_type": measurement_type,
        }
