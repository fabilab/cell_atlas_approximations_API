# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_feature_indices,
    get_feature_names,
    get_homology_distances,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_feature_string,
)


class HomologyDistances(Resource):
    """Get homologous features across species."""

    @required_parameters(
        "source_organism", "target_organism", "source_features", "target_features"
    )
    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        source_organism = args.get("source_organism")
        target_organism = args.get("target_organism")

        source_features = args.get("source_features")
        source_features = clean_feature_string(
            source_features,
            source_organism,
            measurement_type="gene_expression",
        )
        target_features = args.get("target_features")
        target_features = clean_feature_string(
            target_features,
            target_organism,
            measurement_type="gene_expression",
        )

        # NOTE: this is just about capitalisation (should rename it really)
        idxs = get_feature_indices(
            source_organism,
            [fea.lower() for fea in source_features],
            measurement_type="gene_expression",
        )
        features_all = get_feature_names(
            organism=source_organism,
            measurement_type="gene_expression",
        )
        source_features_corrected = list(features_all[idxs])

        # NOTE: this is just about capitalisation (should rename it really)
        idxs = get_feature_indices(
            target_organism,
            [fea.lower() for fea in target_features],
            measurement_type="gene_expression",
        )
        if source_organism != target_organism:
            features_all = get_feature_names(
                organism=target_organism,
                measurement_type="gene_expression",
            )
        target_features_corrected = list(features_all[idxs])

        result = get_homology_distances(
            source_organism,
            source_features_corrected,
            target_organism,
            target_features_corrected,
        )
        result = {
            "queries": result["queries"].values.tolist(),
            "targets": result["targets"].values.tolist(),
            "distances": result["distances"].values.tolist(),
        }

        return result
