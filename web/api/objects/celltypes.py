# Web imports
from flask import request
from flask_restful import Resource

# Helper functions
from models import (
    get_organs,
    get_celltypes,
)


class Celltypes(Resource):
    """Get list of cell types for an organ and organism"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism", None)
        organ = args.get("organ", None)
        if (organism is None) or (organ is None):
            celltypes = None
        elif organ != "whole":
            try:
                celltypes = list(get_celltypes(organism=organism, organ=organ))
            except KeyError:
                celltypes = None
        else:
            organs = get_organs(organism)
            celltypes = set()
            for organ in organs:
                celltypes |= set(get_celltypes(organism=organism, organ=organ))
            celltypes = list(celltypes)

        if celltypes is not None:
            return {
                "organism": organism,
                "organ": organ,
                "celltypes": celltypes,
            }

        # TODO
        return None
