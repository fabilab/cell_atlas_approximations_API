# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_feature_names,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions
)


class Features(Resource):
    """Get list of features for an organism"""

    @required_parameters('organism')
    @model_exceptions
    def get(self):
        """Get list of features (genes)"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")

        features = get_feature_names(
            organism=organism,
            measurement_type=measurement_type,
        )

        return {
            "measurement_type": measurement_type,
            "organism": organism,
            "features": list(features),
        }
