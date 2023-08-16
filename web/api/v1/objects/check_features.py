# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_features,
    OrganismNotFoundError,
    MeasurementTypeNotFoundError,
)
from api.v1.utils import (
    clean_feature_string,
)


class HasFeatures(Resource):
    """Get list of features for an organism"""

    def get(self):
        """Get list of features (genes)"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        features = args.get("features", None)
        if features is None:
            abort(400, message='The "features" parameter is required.')
        try:
            features = clean_feature_string(features, organism, measurement_type)
        except FeatureStringFormatError:
            abort(400, message=f"Feature string not recognised: {features}.")

        try:
            features_all = get_features(
                organism=organism,
                measurement_type=measurement_type,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )

        found_features = [fea in features_all for fea in features]

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "features": features,
            "found": found_features,
        }

