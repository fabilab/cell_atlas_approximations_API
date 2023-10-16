# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_feature_index,
    get_feature_names,
    get_similar_features,
    OrganismNotFoundError,
    OrganNotFoundError,
    FeatureNotFoundError,
    SimilarityMethodError,
    MeasurementTypeNotFoundError,
)
from api.v1.utils import (
    required_parameters,
)


class SimilarFeatures(Resource):
    """Get average measurement by cell type"""

    @required_parameters('organism', 'organ', 'feature', 'number')
    def get(self):
        """Get list of features similar to the focal one"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")
        organ = args.get("organ")
        feature = args.get("feature")
        number = args.get("number")
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

        features_all = get_feature_names(
            organism=organism,
            measurement_type=measurement_type,
        )
        idx = get_feature_index(organism, feature.lower(), measurement_type=measurement_type)
        feature_corrected = features_all[idx]

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "organ": organ,
            "method": method,
            "feature": feature_corrected,
            "similar_features": list(result["features"]),
            "distances": list(result["distances"].astype(float)),
        }
