# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from models import (
    get_fraction_detected,
    get_celltypes,
    get_celltype_location,
    get_feature_index,
    get_feature_names,
    OrganismNotFoundError,
    OrganNotFoundError,
    FeatureNotFoundError,
    TooManyFeaturesError,
    MeasurementTypeNotFoundError,
)
from api.v1.exceptions import FeatureStringFormatError
from api.v1.utils import (
    clean_feature_string,
    clean_organ_string,
    clean_celltype_string,
    required_parameters,
)


class FractionDetected(Resource):
    """Get fraction of detected measurements"""

    @required_parameters('organism', 'features')
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")
        features = args.get("features")
        try:
            features = clean_feature_string(features, organism)
        except FeatureStringFormatError:
            abort(400, message=f"Feature string not recognised: {features}.")

        organ = args.get("organ", None)
        cell_type = args.get("celltype", None)
        if (organ is None) and (cell_type is None):
            abort(400, message='Either "organ" or "celltype" parameter is required.')
        if (organ is not None) and (cell_type is not None):
            abort(400, message='Only one of "organ" or "celltype" parameter can be set.')

        try:
            if organ is not None:
                organ = clean_organ_string(organ)
                avgs = get_fraction_detected(
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
                avgs = get_fraction_detected(
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
        except FeatureNotFoundError:
            abort(400, message="Some features could not be found.")
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
            "fraction_detected": avgs.tolist(),
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
