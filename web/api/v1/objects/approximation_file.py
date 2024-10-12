# Web imports
from flask import (
    request,
    send_file,
)
from flask_restful import Resource

from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from models import get_atlas_path


class ApproximationFile(Resource):
    """Get the static file of an approximation."""

    @required_parameters("organism")
    @model_exceptions
    def get(self):
        """Get a whole approximation."""
        args = request.args
        organism = args.get("organism")

        return send_file(
            get_atlas_path(organism),
            download_name=f"{organism}.h5",
        )
