# Web imports
from flask import request
from flask_restful import Resource

# Helper functions
from models import (
    get_celltypexorganism,
)
from api.v1.exceptions import model_exceptions


class CelltypeXOrganism(Resource):
    """Get list of organs x organism for a cell type"""

    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")

        celltypexorganism = get_celltypexorganism(
            measurement_type=measurement_type,
        )

        organisms = list(celltypexorganism.columns)
        celltypes = list(celltypexorganism.index)
        detected = celltypexorganism.values.tolist()

        return {
            "celltypes": celltypes,
            "measurement_type": measurement_type,
            "organisms": organisms,
            "detected": detected,
        }
