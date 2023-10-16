# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_organs,
    MeasurementTypeNotFoundError,
    OrganismNotFoundError,
)
from api.v1.utils import (
    required_parameters,
)



class Organs(Resource):
    """Get list of tissues for an organism"""

    @required_parameters('organism')
    def get(self):
        """Get list of tissues"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")

        try:
            organs = get_organs(
                organism=organism,
                measurement_type=measurement_type,
            )
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "organs": organs,
        }
