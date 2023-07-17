# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
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
from api.v1.utils import clean_feature_string


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
        celltype = args.get("celltype", None)
        if celltype is None:
            abort(400, message='The "celltype" parameter is required.')
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
            result = get_similar_celltypes(
                organism=organism,
                organ=organ,
                celltype=celltype,
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
            abort(400, message=f"Cell type not found: {celltype}.")
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

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "organ": organ,
            "celltype": celltype,
            "method": method,
            "features": features,
            "similar_celltypes": list(result["celltypes"]),
            "similar_organs": list(result["organs"]),
            "distances": list(result["distances"].astype(float)),
        }
