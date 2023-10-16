# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_organs,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)



class Organs(Resource):
    """Get list of tissues for an organism"""

    @required_parameters('organism')
    @model_exceptions
    def get(self):
        """Get list of tissues"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")

        organs = get_organs(
            organism=organism,
            measurement_type=measurement_type,
        )

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "organs": organs,
        }
