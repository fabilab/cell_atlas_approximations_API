"""Main module for API objects and endpoints"""

from api.endpoints import get_api_endpoint
from api.objects import (
    MeasurementTypes,
    Organisms,
    Organs,
    Celltypes,
    Features,
    Average,
    FractionDetected,
    Markers,
    DataSources,
    HighestMeasurement,
    SimilarFeatures,
    SimilarCelltypes,
    CelltypeXOrgan,
)

__all__ = (
    "api_dict",
    "get_api_endpoint",
)

api_dict = {
    "measurement_types": MeasurementTypes,
    "organisms": Organisms,
    "organs": Organs,
    "features": Features,
    "celltypes": Celltypes,
    "average": Average,
    "fraction_detected": FractionDetected,
    "markers": Markers,
    "highest_measurement": HighestMeasurement,
    "similar_features": SimilarFeatures,
    "similar_celltypes": SimilarCelltypes,
    "celltypexorgan": CelltypeXOrgan,
    "data_sources": DataSources,
}
