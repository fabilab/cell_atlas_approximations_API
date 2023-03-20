# Web imports
from flask import request
from flask_restful import Resource

# Helper functions
from models import (
        get_organs,
    )


class Organs(Resource):
    """Get list of tissues for an organism"""
    def get(self):
        """Get list of tissues"""
        args = request.args
        try:
            organs = get_organs(organism=organism)
        except ValueError:
            organs = None

        if organs is not None:
            return {
                "organism": organism,
                "organs": organs,
            }

        else:
            # TODO
            return None
