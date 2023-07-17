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


class CelltypeXOrgan(Resource):
    """Get list of cell types for an organ and organism"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        organs = args.get("organs", None)
        if organs is not None:
            organs = organs.split(",")
        measurement_type = args.get(
            "measurement_type", "gene_expression")
        boolean = args.get("boolean", False)
        if isinstance(boolean, str):
            boolean = boolean.lower() not in ('false', '0', 'no')

        try:
            celltypexorgan = get_celltypexorgan(
                organism=organism,
                organs=organs,
                measurement_type=measurement_type,
                boolean=boolean,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except OrganNotFoundError:
            abort(400, message="Some organs not found.")
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
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
