# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_organs,
    get_celltypes,
    OrganismNotFoundError,
    OrganNotFoundError,
)


class Celltypes(Resource):
    """Get list of cell types for an organ and organism"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        organ = args.get("organ", None)
        if organ is None:
            abort(400, message='The "organ" parameter is required.')

        try:
            celltypes = list(get_celltypes(organism=organism, organ=organ))
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except OrganNotFoundError:
            abort(400, message=f"Organ not found: {organ}.")

        return {
            "organism": organism,
            "organ": organ,
            "celltypes": celltypes,
        }
