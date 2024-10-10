# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_organs,
    get_celltypes,
    get_celltype_abundance,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_organ_string,
)


class Celltypes(Resource):
    """Get list of cell types for an organ and organism"""

    @required_parameters("organism", "organ")
    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        organism = args.get("organism")
        organ = args.get("organ")
        organ = clean_organ_string(organ)
        measurement_type = args.get("measurement_type", "gene_expression")
        include_abundance = (
            str(args.get("include_abundance", "false")).lower() != "false"
        )

        if include_abundance:
            res = get_celltype_abundance(
                organism=organism, organ=organ, measurement_type=measurement_type
            )
            celltypes = list(res.index)
            # Numpy integers are not serialisable
            abundance = [int(x) for x in res.values]
            del res
        else:
            celltypes = list(
                get_celltypes(
                    organism=organism, organ=organ, measurement_type=measurement_type
                )
            )

        result = {
            "organism": organism,
            "organ": organ,
            "measurement_type": measurement_type,
            "celltypes": celltypes,
        }

        if include_abundance:
            result["abundance"] = abundance

        return result
