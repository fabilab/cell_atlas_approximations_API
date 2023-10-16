# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_feature_index,
    get_feature_names,
    get_similar_celltypes,
)
from api.v1.exceptions import (
    FeatureStringFormatError,
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_feature_string,
    clean_organ_string,
    clean_celltype_string,
)


class SimilarCelltypes(Resource):
    """Get average measurement by cell type"""

    @required_parameters('organism', 'organ', 'celltype', 'features', 'number')
    @model_exceptions
    def get(self):
        """Get list of features similar to the focal one"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")
        organ = args.get("organ")
        organ = clean_organ_string(organ)
        cell_type = args.get("celltype")
        cell_type = clean_celltype_string(cell_type)
        features = args.get("features")
        features = clean_feature_string(features, organism)

        number = args.get("number")
        method = args.get("method", "correlation")
        try:
            number = int(number)
        except (TypeError, ValueError):
            abort(400, message='The "number" parameter should be an integer.')
        if number <= 0:
            abort(400, message='The "number" parameter should be positive.')

        # NOTE: method can change if there is only one feature, because
        # correlation-like methods are undefined
        result = get_similar_celltypes(
            organism=organism,
            organ=organ,
            celltype=cell_type,
            features=features,
            number=number,
            method=method,
            measurement_type=measurement_type,
        )

        features_corrected = []
        features_all = get_feature_names(
            organism=organism,
            measurement_type=measurement_type,
        )
        for fea in features:
            idx = get_feature_index(organism, fea.lower(), measurement_type=measurement_type)
            features_corrected.append(features_all[idx])

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "organ": organ,
            "celltype": cell_type,
            "method": result['method'],
            "features": features_corrected,
            "similar_celltypes": list(result["celltypes"]),
            "similar_organs": list(result["organs"]),
            "distances": list(result["distances"].astype(float)),
        }
