# Web imports
from flask import request
from flask_restful import Resource

# Helper functions
from models import (
    get_fraction_detected,
)


class FractionDetected(Resource):
    """Get fraction of detected measurements"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism", None)
        organ = args.get("organ", None)
        features = args.get("features", None)
        if (organism is None) or (organ is None) or (features is None):
            avgs = None
        else:
            features = features.split(",")
            try:
                avgs = get_fraction_detected(
                    organism=organism,
                    organ=organ,
                    features=features,
                )
            except KeyError:
                avgs = None

        if avgs is not None:
            return {
                "organism": organism,
                "organ": organ,
                "features": features,
                "fraction_detected": avgs.tolist(),
            }

        # TODO
        return None
