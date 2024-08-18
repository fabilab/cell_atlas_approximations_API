# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_markers_vs_other_celltypes,
    get_markers_vs_other_tissues,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_organ_string,
    clean_celltype_string,
)


class Markers(Resource):
    """Get average measurement by cell type"""

    @required_parameters('organism', 'organ', 'celltype', 'number')
    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")
        organ = args.get("organ")
        organ = clean_organ_string(organ)
        cell_type = args.get("celltype")
        cell_type = clean_celltype_string(cell_type)
        number = args.get("number")
        versus = args.get("versus", "other_celltypes")
        surface_only = str(args.get("surface_only", 'false')).lower() != 'false'

        if versus not in ("other_celltypes", "other_organs"):
            abort(
                400,
                message='The "versus" parameter should be either "other_celltypes" or "other_organs".')

        try:
            number = int(number)
        except (TypeError, ValueError):
            abort(400, message='The "number" parameter should be an integer.')

        if number <= 0:
            abort(400, message='The "number" parameter should be positive.')

        if versus == "other_celltypes":
            markers = get_markers_vs_other_celltypes(
                organism=organism,
                organ=organ,
                cell_type=cell_type,
                number=number,
                measurement_type=measurement_type,
                surface_only=surface_only,
            )
            if cell_type == 'all':
                markers, targets = markers
        else:
            markers = get_markers_vs_other_tissues(
                organism=organism,
                organ=organ,
                cell_type=cell_type,
                number=number,
                measurement_type=measurement_type,
                surface_only=surface_only,
            )
            if organ == 'all':
                markers, targets = markers

        result =  {
            "organism": organism,
            "organ": organ,
            "measurement_type": measurement_type,
            "celltype": cell_type,
            "markers": list(markers),
        }

        if (versus == "other_celltypes") and (cell_type == 'all'):
            result['targets'] = targets
        elif (versus == "other_organs") and (organ == 'all'):
            result['targets'] = targets

        return result
