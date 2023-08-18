# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from config import configuration as config
from models import (
    get_averages,
    get_celltypes,
    get_celltype_location,
    get_feature_index,
    get_feature_names,
    OrganismNotFoundError,
    OrganNotFoundError,
    CellTypeNotFoundError,
    SomeFeaturesNotFoundError,
    TooManyFeaturesError,
    MeasurementTypeNotFoundError,
)
from api.v1.exceptions import FeatureStringFormatError
from api.v1.utils import (
    clean_feature_string,
    clean_organ_string,
    clean_celltype_string,
)


class Average(Resource):
    """Get average measurement by cell type"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism", None)
        if organism is None:
            abort(400, message='The "organism" parameter is required.')
        features = args.get("features", None)
        if features is None:
            abort(400, message='The "features" parameter is required.')
        try:
            features = clean_feature_string(features, organism, measurement_type)
        except FeatureStringFormatError:
            abort(400, message=f"Feature string not recognised: {features}.")
        unit = config['units'][measurement_type]

        organ = args.get("organ", None)
        cell_type = args.get("celltype", None)
        if (organ is None) and (cell_type is None):
            abort(400, message='Either "organ" or "celltype" parameter is required.')
        if (organ is not None) and (cell_type is not None):
            abort(400, message='Only one of "organ" or "celltype" parameter can be set.')

        try:
            if organ is not None:
                organ = clean_organ_string(organ)
                avgs = get_averages(
                    organism=organism,
                    organ=organ,
                    features=features,
                    measurement_type=measurement_type,
                )
                cell_types = list(get_celltypes(
                    organism=organism,
                    organ=organ,
                    measurement_type=measurement_type,
                ))
            else:
                cell_type = clean_celltype_string(cell_type)
                avgs = get_averages(
                    organism=organism,
                    cell_type=cell_type,
                    features=features,
                    measurement_type=measurement_type,
                )
                organs = list(get_celltype_location(
                    organism=organism,
                    cell_type=cell_type,
                    measurement_type=measurement_type,
                ))
        except OrganismNotFoundError:
            abort(400, message=f"Organism not found: {organism}.")
        except OrganNotFoundError:
            abort(400, message=f"Organ not found: {organ}.")
        except CellTypeNotFoundError:
            abort(400, message=f"Cell type not found: {cell_type}.")
        except SomeFeaturesNotFoundError as exc:
            abort(
                400,
                message="Some features could not be found.",
                missing=exc.features,
            )
        except TooManyFeaturesError:
            abort(
                400,
                message=f"Maximal number of features is 50. Requested: {len(features)}.",
            )
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
            )

        features_corrected = []
        features_all = get_feature_names(
            organism=organism,
            measurement_type=measurement_type,
        )
        for fea in features:
            idx = get_feature_index(organism, fea.lower(), measurement_type=measurement_type)
            features_corrected.append(features_all[idx])

        result = {
            "organism": organism,
            "measurement_type": measurement_type,
            "features": features_corrected,
            "average": avgs.tolist(),
            "unit": unit,
        }
        if organ is not None:
            result.update({
                "organ": organ,
                "celltypes": cell_types,
            })
        else:
            result.update({
                "organs": organs,
                "celltype": cell_type,
            })
        return result

