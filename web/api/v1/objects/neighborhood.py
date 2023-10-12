# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from config import configuration as config
from models import (
    get_neighborhoods,
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


class Neighborhood(Resource):
    """Get average measurement by cell type"""

    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism", None)
        if organism is None:
            abort(
                400,
                message='The "organism" parameter is required.',
                exception='missing_parameter=organism',
            )
        features = args.get("features", None)
        if features is None:
            abort(
                400,
                message='The "features" parameter is required.',
                exception='missing_parameter=features',
            )
        try:
            features = clean_feature_string(features, organism, measurement_type)
        except FeatureStringFormatError:
            abort(
                400,
                message=f"Feature string not recognised: {features}.",
                exception='invalid_parameter=features',
            )
        unit = config['units'][measurement_type]

        organ = args.get("organ", None)
        if organ is None:
            abort(400, message='The "organ" parameter is required.')

        try:
            organ = clean_organ_string(organ)
            neis = get_neighborhoods(
                organism=organism,
                organ=organ,
                features=features,
                measurement_type=measurement_type,
            )
        except OrganismNotFoundError:
            abort(
                400,
                message=f"Organism not found: {organism}.",
                exception="invalid_parameter=organism",
            )
        except OrganNotFoundError:
            abort(
                400,
                message=f"Organ not found: {organ}.",
                exception="invalid_parameter=organ",
            )
        except SomeFeaturesNotFoundError as exc:
            abort(
                400,
                message="Some features could not be found.",
                exception="invalid_parameter=features",
                missing=exc.features,
            )
        except TooManyFeaturesError:
            abort(
                400,
                message=f"Too many features requested: {len(features)}.",
                exception="too_large_parameter=features",
            )
        except MeasurementTypeNotFoundError:
            abort(
                400,
                message=f"Measurement type not found: {measurement_type}.",
                exception="invalid_parameter=measurement_type",
            )

        # Unpack neighborhood data for output
        avgs = neis['average']
        cell_types = neis['celltype']
        coords_centroid = neis['coords_centroid']
        convex_hulls = [hull.tolist() for hull in neis['convex_hull']]

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
            "celltypes": cell_types.tolist(),
            "coords_centroid": coords_centroid.tolist(),
            "convex_hull": convex_hulls,
            "unit": unit,
            "organ": organ,
        }
        if 'frac' in neis:
            result["fraction_detected"] = neis['fraction'].tolist()

        return result

