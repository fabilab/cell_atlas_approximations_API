# Web imports
from flask_restful import Resource

# Helper functions
from models import (
    get_data_sources,
)
from api.v1.exceptions import (
    model_exceptions,
)


class DataSources(Resource):
    """Get list of organisms"""

    @model_exceptions
    def get(self):
        """Get list of organisms"""
        return get_data_sources()
