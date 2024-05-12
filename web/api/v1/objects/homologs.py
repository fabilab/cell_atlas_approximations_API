# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_feature_index,
    get_feature_names,
    get_homologs,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_feature_string,
)


class Homologs(Resource):
    """Get homologous features across species."""

    @required_parameters('source_organism', 'target_organism', 'features')
    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        source_organism = args.get("source_organism")
        target_organism = args.get("target_organism")
        if source_organism == target_organism:
            abort(
                400,
                message=f"Source and target organisms cannot be the same: {source_organism}.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "organism",
                    "invalid_value": source_organism,
                }
            )

        features = args.get("features")
        features = clean_feature_string(
            features, source_organism, measurement_type="gene_expression",
        )

        # NOTE: this is just about capitalisation (should rename it really)
        features_corrected = []
        features_all = get_feature_names(
            organism=source_organism,
            measurement_type="gene_expression",
        )
        for fea in features:
            idx = get_feature_index(source_organism, fea.lower(),
                                    measurement_type="gene_expression")
            features_corrected.append(features_all[idx])

        result = get_homologs(
            source_organism,
            features_corrected,
            target_organism,
        )

        return result
