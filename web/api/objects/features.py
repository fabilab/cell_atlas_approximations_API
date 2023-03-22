# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_features,
    OrganismNotFoundError,
)


class Features(Resource):
    """Get list of features for an organism"""

    def get(self):
        """Get list of features (genes)"""
        args = request.args
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')

        try:
            features = get_features(organism=organism)
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")

        return {
            "organism": organism,
            "features": list(features),
        }
