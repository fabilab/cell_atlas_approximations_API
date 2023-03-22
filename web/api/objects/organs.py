# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_organs,
    OrganismNotFoundError,
)


class Organs(Resource):
    """Get list of tissues for an organism"""

    def get(self):
        """Get list of tissues"""
        args = request.args
        organism = args.get("organism", None)

        if organism is None:
            abort(400, message="The \"organism\" parameter is required.")
        else:
            try:
                organs = get_organs(organism=organism)
            except OrganismNotFoundError:
                abort(400, message=f"Organism not found: {organism}.")

        return {
            "organism": organism,
            "organs": organs,
        }
