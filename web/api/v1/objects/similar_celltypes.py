# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_feature_index,
    get_feature_names,
    get_similar_celltypes,
    OrganismNotFoundError,
    OrganNotFoundError,
    FeatureNotFoundError,
    TooManyFeaturesError,
    SimilarityMethodError,
    CellTypeNotFoundError,
    MeasurementTypeNotFoundError,
)
from api.v1.exceptions import FeatureStringFormatError
from api.v1.utils import (
    clean_feature_string,
    clean_organ_string,
    clean_celltype_string,
)


class SimilarCelltypes(Resource):
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
        organ = clean_organ_string(organ)
        cell_type = args.get("celltype", None)
        if cell_type is None:
            abort(400, message='The "celltype" parameter is required.')
        cell_type = clean_celltype_string(cell_type)
        features = args.get("features", None)
        if features is None:
            abort(400, message='The "features" parameter is required.')
        try:
            features = clean_feature_string(features, organism)
        except FeatureStringFormatError:
            abort(400, message=f"Feature string not recognised: {features}.")

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

        try:
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
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except OrganNotFoundError:
            abort(400, message=f"Organ not found: {organ}.")
        except CellTypeNotFoundError:
            abort(400, message=f"Cell type not found: {cell_type}.")
        except FeatureNotFoundError:
            abort(400, message="Some features could not be found.")
        except TooManyFeaturesError:
            abort(
                400,
                message=f"Maximal number of features is 50. Requested: {len(features)}.",
            )
        except SimilarityMethodError:
            abort(400, message=f"Similarity method not supported: {method}.")
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
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
