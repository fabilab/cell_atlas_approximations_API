# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_feature_index,
    get_feature_names,
    get_interaction_partners,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_feature_string,
)


class InteractionPartners(Resource):
    """Get partners of established cell-cell interactions"""

    @required_parameters('organism', 'features')
    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")
        features = args.get("features")
        features = clean_feature_string(features, organism, measurement_type)

        # NOTE: this is just about capitalisation (should rename it really)
        features_corrected = []
        features_all = get_feature_names(
            organism=organism,
            measurement_type=measurement_type,
        )
        for fea in features:
            idx = get_feature_index(organism, fea.lower(), measurement_type=measurement_type)
            features_corrected.append(features_all[idx])

        result = get_interaction_partners(
            organism,
            features_corrected,
            measurement_type=measurement_type,
        )

        return result
