# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_features,
    get_feature_index,
    get_feature_names,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_feature_string,
)


class HasFeatures(Resource):
    """Get list of features for an organism"""

    @required_parameters('organism', 'features')
    @model_exceptions
    def get(self):
        """Get list of features (genes)"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")
        features = args.get("features")
        features = clean_feature_string(features, organism, measurement_type)

        features_lowercase = get_features(
            organism=organism,
            measurement_type=measurement_type,
        )

        is_found = []
        features_corrected = []
        features_all = get_feature_names(
            organism=organism,
            measurement_type=measurement_type,
        )
        for fea in features:
            if fea.lower() not in features_lowercase:
                is_found.append(False)
                features_corrected.append(fea)
            else:
                is_found.append(True)
                idx = get_feature_index(organism, fea.lower(), measurement_type=measurement_type)
                features_corrected.append(features_all[idx])

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "features": features_corrected,
            "found": is_found,
        }

