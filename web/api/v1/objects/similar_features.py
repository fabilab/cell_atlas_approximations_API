# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_similar_features,
    OrganismNotFoundError,
    OrganNotFoundError,
    FeatureNotFoundError,
    SimilarityMethodError,
    MeasurementTypeNotFoundError,
)


class SimilarFeatures(Resource):
    """Get average measurement by cell type"""

    def get(self):
        """Get list of features similar to the focal one"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        organ = args.get("organ", None)
        if organ is None:
            abort(400, message='The "organ" parameter is required.')
        feature = args.get("feature", None)
        if feature is None:
            abort(400, message='The "feature" parameter is required.')
        number = args.get("number", None)
        if number is None:
            abort(400, message='The "number" parameter is required.')
        method = args.get("method", "correlation")

        try:
            number = int(number)
        except (TypeError, ValueError):
            abort(400, message='The "number" parameter should be an integer.')
        if number <= 0:
            abort(400, message='The "number" parameter should be positive.')
        elif number > 50:
            abort(
                400,
                message=f"Max number of similar features is 50, requested: {number}.",
            )

        try:
            result = get_similar_features(
                organism=organism,
                organ=organ,
                feature_name=feature,
                number=number,
                method=method,
                measurement_type=measurement_type,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except OrganNotFoundError:
            abort(400, message=f"Organ not found: {organ}.")
        except FeatureNotFoundError:
            abort(400, message=f"Feature not found: {feature}.")
        except SimilarityMethodError:
            abort(400, message=f"Similarity method not supported: {method}.")
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "organ": organ,
            "method": method,
            "feature": feature,
            "similar_features": list(result["features"]),
            "distances": list(result["distances"].astype(float)),
        }
