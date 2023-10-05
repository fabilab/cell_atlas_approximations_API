# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_features,
    get_feature_index,
    get_feature_names,
    get_feature_sequences,
    OrganismNotFoundError,
    MeasurementTypeNotFoundError,
)
from api.v1.exceptions import FeatureStringFormatError
from api.v1.utils import (
    clean_feature_string,
)


class FeatureSequences(Resource):
    """Get list of features for an organism"""

    def get(self):
        """Get list of features (genes)"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        features = args.get("features", None)
        if features is None:
            abort(400, message='The "features" parameter is required.')
        try:
            features = clean_feature_string(features, organism, measurement_type)
        except FeatureStringFormatError:
            abort(400, message=f"Feature string not recognised: {features}.")

        try:
            features_lowercase = get_features(
                organism=organism,
                measurement_type=measurement_type,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
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
