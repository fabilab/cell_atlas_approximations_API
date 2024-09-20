# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from config import configuration as config
from models import (
    get_feature_index,
    get_feature_names,
    get_highest_measurement_multiple,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_feature_string,
)


class HighestMeasurementMultiple(Resource):
    """Get measurement in highest cell types"""

    @required_parameters('organism', 'features', 'number')
    @model_exceptions
    def get(self):
        """Get expression in highest cell types, in one organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")
        features = args.get("features")
        features = clean_feature_string(features, organism, measurement_type)
        features_neg = args.get("features_negative")
        features_neg = clean_feature_string(features_neg, organism, measurement_type)
        number = args.get("number")
        unit = config["units"][measurement_type]
        per_organ = str(args.get("per_organ", 'false')).lower() != 'false'

        try:
            number = int(number)
        except (TypeError, ValueError):
            abort(400, message='The "number" parameter should be an integer.')

        if number <= 0:
            abort(400, message='The "number" parameter should be positive.')

        result = get_highest_measurement_multiple(
            organism=organism,
            features=features,
            features_negative=features_neg,
            number=number,
            measurement_type=measurement_type,
            per_organ=per_organ,
        )
        features = result["features"]
        features_neg = result.get("features_negative", [])

        # NOTE: this is just about capitalisation (should rename it really)
        features_corrected = []
        features_neg_corrected = []
        features_all = get_feature_names(
            organism=organism,
            measurement_type=measurement_type,
        )
        for fea in features:
            idx = get_feature_index(organism, fea.lower(), measurement_type=measurement_type)
            features_corrected.append(features_all[idx])
        for fea in features_neg:
            idx = get_feature_index(organism, fea.lower(), measurement_type=measurement_type)
            features_neg_corrected.append(features_all[idx])


        result = {
            "measurement_type": measurement_type,
            "organism": organism,
            "features": features_corrected,
            "organs": result["organs"],
            "celltypes": result["celltypes"],
            "average": result["average"].tolist(),
            "fraction_detected": result["fraction_detected"].tolist(),
            "score": result["score"].tolist(),
            "unit": unit,
        }
        if len(features_neg_corrected) > 0:
            result["features_negative"] = features_neg_corrected

        return result
