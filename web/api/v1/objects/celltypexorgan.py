# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_celltypexorgan,
    OrganismNotFoundError,
    OrganNotFoundError,
    MeasurementTypeNotFoundError,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions
)


class CelltypeXOrgan(Resource):
    """Get list of cell types for an organ and organism"""

    @required_parameters('organism')
    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism")
        organs = args.get("organs", None)
        if organs is not None:
            organs = organs.split(",")
        measurement_type = args.get(
            "measurement_type", "gene_expression")
        boolean = args.get("boolean", False)
        if isinstance(boolean, str):
            boolean = boolean.lower() not in ('false', '0', 'no')

        celltypexorgan = get_celltypexorgan(
            organism=organism,
            organs=organs,
            measurement_type=measurement_type,
            boolean=boolean,
        )

        organs = list(celltypexorgan.columns)
        celltypes = list(celltypexorgan.index)
        detected = celltypexorgan.values.tolist()

        return {
            "organism": organism,
            "measurement_type": measurement_type,
            "organs": organs,
            "celltypes": celltypes,
            "detected": detected,
        }
