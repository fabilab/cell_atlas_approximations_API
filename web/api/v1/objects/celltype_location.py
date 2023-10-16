# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_celltype_location,
    OrganismNotFoundError,
    CellTypeNotFoundError,
    MeasurementTypeNotFoundError,
)
from api.v1.utils import (
    clean_celltype_string,
    required_parameters,
)


class CelltypeLocation(Resource):
    """Get list of cell types for an organ and organism"""

    @required_parameters('organism', 'celltype')
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism")
        cell_type = args.get("celltype")
        cell_type = clean_celltype_string(cell_type)
        measurement_type = args.get(
            "measurement_type", "gene_expression")

        try:
            organs = get_celltype_location(
                organism=organism,
                cell_type=cell_type,
                measurement_type=measurement_type,
            )
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except CellTypeNotFoundError:
            abort(400, message=f"Cell type not found: {cell_type}.")
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )
        organs = list(organs)

        return {
            "organism": organism,
            "measurement_type": measurement_type,
            "celltype": cell_type,
            "organs": organs,
        }
