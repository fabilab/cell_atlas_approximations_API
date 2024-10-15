# Web imports
from flask_restful import Resource

# Helper functions
from models import (
    get_full_atlas_files,
)
from api.v1.exceptions import (
    model_exceptions,
)


class FullAtlasFiles(Resource):
    """Get list of organisms"""

    @model_exceptions
    def get(self):
        """Get list of organisms"""
        return get_full_atlas_files()
