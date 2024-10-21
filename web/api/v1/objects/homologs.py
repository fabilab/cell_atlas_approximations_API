# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_feature_indices,
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

    @required_parameters("source_organism", "target_organism", "features")
    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        source_organism = args.get("source_organism")
        target_organism = args.get("target_organism")

        features = args.get("features")
        features = clean_feature_string(
            features,
            source_organism,
            measurement_type="gene_expression",
        )
        max_distance_over_min = args.get(
            "max_distance_over_min", type=float, default=8.0
        )
        if (max_distance_over_min is None) or (max_distance_over_min < 0):
            abort(
                400,
                message="If specified, max_distance_over_min must be a nonnegative number.",
            )

        # NOTE: this is just about capitalisation (should rename it really)
        idxs = get_feature_indices(
            source_organism,
            [fea.lower() for fea in features],
            measurement_type="gene_expression",
        )
        features_all = get_feature_names(
            organism=source_organism,
            measurement_type="gene_expression",
        )
        features_corrected = list(features_all[idxs])

        result = get_homologs(
            source_organism,
            features_corrected,
            target_organism,
            max_distance_over_min=max_distance_over_min,
        )

        return result
