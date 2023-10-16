# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_features,
    get_feature_index,
    get_feature_names,
    get_feature_sequences,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_feature_string,
)


class FeatureSequences(Resource):
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

        features_corrected = []
        sequences = []
        features_all = get_feature_names(
            organism=organism,
            measurement_type=measurement_type,
        )
        for fea in features:
            if fea.lower() not in features_lowercase:
                features_corrected.append(fea)
            else:
                idx = get_feature_index(organism, fea.lower(), measurement_type=measurement_type)
                features_corrected.append(features_all[idx])

        features, sequences, sequence_type = get_feature_sequences(
            organism,
            features_corrected,
            measurement_type=measurement_type,
        )

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "features": list(features),
            "sequences": list(sequences),
            "type": sequence_type,
        }
