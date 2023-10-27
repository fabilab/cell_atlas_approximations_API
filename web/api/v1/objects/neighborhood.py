# Web imports
from flask import request
from flask_restful import Resource, abort

# Helper functions
from config import configuration as config
from models import (
    get_celltypes,
    get_neighborhoods,
    get_feature_index,
    get_feature_names,
)
from api.v1.exceptions import (
    required_parameters,
    model_exceptions,
)
from api.v1.utils import (
    clean_feature_string,
    clean_organ_string,
    clean_celltype_string,
)


class Neighborhood(Resource):
    """Get average measurement by cell type"""

    @required_parameters('organism', 'organ')
    @model_exceptions
    def get(self):
        """Get list of cell types for an organ and organism"""
        args = request.args
        measurement_type = args.get("measurement_type", "gene_expression")
        organism = args.get("organism")
        organ = args.get("organ")
        organ = clean_organ_string(organ)
        features = args.get("features", None)
        if features is not None:
            features = clean_feature_string(features, organism, measurement_type)
        unit = config['units'][measurement_type]

        include_embedding = bool(args.get("include_embedding", False))

        neis = get_neighborhoods(
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

        # Unpack neighborhood data for output
        ncells_per_cluster = neis['ncells']
        if include_embedding:
            coords_centroid = neis['coords_centroid']
            convex_hulls = [hull.tolist() for hull in neis['convex_hull']]

        if (features is not None) and len(features):
            features_corrected = []
            features_all = get_feature_names(
                organism=organism,
                measurement_type=measurement_type,
            )
            for fea in features:
                idx = get_feature_index(organism, fea.lower(), measurement_type=measurement_type)
                features_corrected.append(features_all[idx])

        result = {
            "measurement_type": measurement_type,
            "organism": organism,
            "organ": organ,
            "ncells": ncells_per_cluster.tolist(),
            "celltypes": cell_types,
        }
        if (features is not None) and len(features):
            result.update({
                "average": neis['average'].tolist(),
                "features": features_corrected,
                "unit": unit,
            })
        if 'fraction' in neis:
            result["fraction_detected"] = neis['fraction'].tolist()

        if include_embedding:
            result.update({
                "centroids": coords_centroid.tolist(),
                "boundaries": convex_hulls,
            })

        return result

