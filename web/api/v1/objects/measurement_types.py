# Web imports
from flask import request
from flask_restful import Resource

# Helper functions
from config import configuration as config


class MeasurementTypes(Resource):
    """Get list of measurement types."""

    def get(self):
        """Get list of measurement types."""
        measurement_types = config['feature_types']
        return {
            "measurement_types": measurement_types,
        }
