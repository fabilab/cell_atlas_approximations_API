"""Main module for API v1"""
from api.v1.endpoints import get_api_endpoint
from api.v1.objects import (
    MeasurementTypes,
    Organisms,
    Organs,
    Celltypes,
    Dotplot,
    HasFeatures,
    Features,
    FeatureSequences,
    Average,
    FractionDetected,
    Markers,
    DataSources,
    HighestMeasurement,
    HighestMeasurementMultiple,
    SimilarFeatures,
    SimilarCelltypes,
    CelltypeXOrgan,
    OrganXOrganism,
    CelltypeLocation,
    Neighborhood,
    InteractionPartners,
    Homologs,
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
        "dotplot": Dotplot,
        "neighborhood": Neighborhood,
        "markers": Markers,
        "interaction_partners": InteractionPartners,
        "homologs": Homologs,
        "highest_measurement": HighestMeasurement,
        "highest_measurement_multiple": HighestMeasurementMultiple,
        "similar_features": SimilarFeatures,
        "similar_celltypes": SimilarCelltypes,
        "celltypexorgan": CelltypeXOrgan,
        "organxorganism": OrganXOrganism,
        "celltype_location": CelltypeLocation,
        "data_sources": DataSources,
    }
}
