# Web imports
from flask import request
from flask_restful import Resource

# Helper functions
from models import (
    get_organisms,
)


class Organisms(Resource):
    """Get list of organisms"""

    def get(self):
        """Get list of organisms"""
        organisms = get_organisms()
        return {
            "organisms": organisms,
        }
