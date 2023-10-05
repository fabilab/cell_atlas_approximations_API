"""Main module for API v1"""
from api.v1.endpoints import get_api_endpoint
from api.v1.objects import (
    MeasurementTypes,
    Organisms,
    Organs,
    Celltypes,
    HasFeatures,
    Features,
    FeatureSequences,
    Average,
    FractionDetected,
    Markers,
    DataSources,
    HighestMeasurement,
    SimilarFeatures,
    SimilarCelltypes,
    CelltypeXOrgan,
    CelltypeLocation,
)

__all__ = (
    "api_dict",
)

api_dict = {
    "endpoint_handler": get_api_endpoint,
    "objects": {
        "measurement_types": MeasurementTypes,
        "organisms": Organisms,
        "organs": Organs,
        "features": Features,
        "sequences": FeatureSequences,
        "has_features": HasFeatures,
        "celltypes": Celltypes,
        "average": Average,
        "fraction_detected": FractionDetected,
        "markers": Markers,
        "highest_measurement": HighestMeasurement,
        "similar_features": SimilarFeatures,
        "similar_celltypes": SimilarCelltypes,
        "celltypexorgan": CelltypeXOrgan,
        "celltype_location": CelltypeLocation,
        "data_sources": DataSources,
    }
}
