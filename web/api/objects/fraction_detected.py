# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_fraction_detected,
    get_celltypes,
    OrganismNotFoundError,
    OrganNotFoundError,
    FeatureNotFoundError,
    TooManyFeaturesError,
)
from api.exceptions import FeatureStringFormatError
from api.utils import clean_feature_string


class FractionDetected(Resource):
    """Get fraction of detected measurements"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        organ = args.get("organ", None)
        if organ is None:
            abort(400, message='The "organ" parameter is required.')
        features = args.get("features", None)
        if features is None:
            abort(400, message='The "features" parameter is required.')
        try:
            features = clean_feature_string(features, organism)
        except FeatureStringFormatError:
            abort(400, message=f"Feature string not recognised: {features}.")
        unit = "fraction"

        try:
            avgs = get_fraction_detected(
                organism=organism,
                organ=organ,
                features=features,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except OrganNotFoundError:
            abort(400, message=f"Organ not found: {organ}.")
        except FeatureNotFoundError:
            abort(400, message="Some features could not be found.")
        except TooManyFeaturesError:
            abort(
                400,
                message=f"Maximal number of features is 50. Requested: {len(features)}.",
            )

        # This cannot fail since the exceptions above were survived already
        cell_types = list(get_celltypes(
            organism=organism,
            organ=organ,
        ))

        return {
            "organism": organism,
            "organ": organ,
            "features": features,
            "fraction_detected": avgs.tolist(),
            "celltypes": cell_types,
            "unit": unit,
        }
