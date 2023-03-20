# Web imports
from flask import request
from flask_restful import Resource

# Helper functions
from models import (
    get_features,
)


class Features(Resource):
    """Get list of features for an organism"""

    def get(self):
        """Get list of features (genes)"""
        args = request.args
        organism = args.get("organism", None)
        if organism is None:
            features = None
        else:
            try:
                features = get_features(organism=organism)
            except KeyError:
                features = None

        if features is not None:
            return {
                "organism": organism,
                "features": list(features),
            }

        # TODO
        return None
