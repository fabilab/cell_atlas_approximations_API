# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from config import configuration as config
from models import (
    get_feature_index,
    get_feature_names,
    get_highest_measurement,
    OrganismNotFoundError,
    FeatureNotFoundError,
    MeasurementTypeNotFoundError,
)


class HighestMeasurement(Resource):
    """Get measurement in highest cell types"""

    def get(self):
        """Get expression in highest cell types, in one organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        feature = args.get("feature", None)
        if feature is None:
            abort(400, message='The "feature" parameter is required.')
        unit = config["units"][measurement_type]
        number = args.get("number", None)
        if number is None:
            abort(400, message='The "number" parameter is required.')

        try:
            number = int(number)
        except (TypeError, ValueError):
            abort(400, message='The "number" parameter should be an integer.')

        if number <= 0:
            abort(400, message='The "number" parameter should be positive.')

        try:
            result = get_highest_measurement(
                organism=organism,
                feature=feature,
                number=number,
                measurement_type=measurement_type,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except FeatureNotFoundError:
            abort(400, message="Some features could not be found.")
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )

        features_all = get_feature_names(
            organism=organism,
            measurement_type=measurement_type,
        )
        idx = get_feature_index(organism, feature.lower(), measurement_type=measurement_type)
        feature_corrected = features_all[idx]

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "feature": feature_corrected,
            "organs": result["organs"],
            "celltypes": result["celltypes"],
            "average": result["average"].tolist(),
            "unit": unit,
        }
