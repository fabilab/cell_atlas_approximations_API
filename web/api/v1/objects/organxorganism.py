# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_organxorganism,
    MeasurementTypeNotFoundError,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions
)
from api.v1.utils import (
    clean_celltype_string,
)


class OrganXOrganism(Resource):
    """Get list of organs x organism for a cell type"""

    @required_parameters('celltype')
    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        cell_type = args.get("celltype")
        cell_type = clean_celltype_string(cell_type)
        measurement_type = args.get(
            "measurement_type", "gene_expression")

        organxorganism = get_organxorganism(
            cell_type,
            measurement_type=measurement_type,
        )

        organisms = list(organxorganism.columns)
        organs = list(organxorganism.index)
        detected = organxorganism.values.tolist()

        return {
            "celltype": cell_type,
            "measurement_type": measurement_type,
            "organs": organs,
            "organisms": organisms,
            "detected": detected,
        }
