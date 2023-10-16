# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_celltype_location,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_celltype_string,
)


class CelltypeLocation(Resource):
    """Get list of cell types for an organ and organism"""

    @required_parameters('organism', 'celltype')
    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism")
        cell_type = args.get("celltype")
        cell_type = clean_celltype_string(cell_type)
        measurement_type = args.get(
            "measurement_type", "gene_expression")

        organs = get_celltype_location(
            organism=organism,
            cell_type=cell_type,
            measurement_type=measurement_type,
        )
        organs = list(organs)

        return {
            "organism": organism,
            "measurement_type": measurement_type,
            "celltype": cell_type,
            "organs": organs,
        }
