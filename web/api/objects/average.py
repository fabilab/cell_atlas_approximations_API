# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from config import configuration as config
from models import (
    get_averages,
    get_celltypes,
    OrganismNotFoundError,
    OrganNotFoundError,
    FeatureNotFoundError,
    TooManyFeaturesError,
    MeasurementTypeNotFoundError,
)
from api.exceptions import FeatureStringFormatError
from api.utils import clean_feature_string


class Average(Resource):
    """Get average measurement by cell type"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        organ = args.get("organ", None)
        if organ is None:
            abort(400, message='The "organ" parameter is required.')
        features = args.get("features", None)
        if features is None:
            abort(400, message='The "features" parameter is required.')
        try:
            features = clean_feature_string(features, organism, measurement_type)
        except FeatureStringFormatError:
            abort(400, message=f"Feature string not recognised: {features}.")
        unit = config['units'][measurement_type]

        try:
            avgs = get_averages(
                organism=organism,
                organ=organ,
                features=features,
                measurement_type=measurement_type,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except OrganNotFoundError:
            abort(400, message=f"Organ not found: {organ}.")
        except FeatureNotFoundError:
            abort(400, message="Some features could not be found.")
        except TooManyFeaturesError:
            abort(
                400,
                message=f"Maximal number of features is 50. Requested: {len(features)}.",
            )
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )

        # This cannot fail since the exceptions above were survived already
        cell_types = list(get_celltypes(
            organism=organism,
            organ=organ,
            measurement_type=measurement_type,
        ))

        return {
            "organism": organism,
            "organ": organ,
            "measurement_type": measurement_type,
            "features": features,
            "average": avgs.tolist(),
            "celltypes": cell_types,
            "unit": unit,
        }
