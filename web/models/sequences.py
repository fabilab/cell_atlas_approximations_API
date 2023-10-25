"""Feature sequences (e.g. genes, transcripts, peaks)"""
from config import configuration as config
from models.paths import get_atlas_path
from models.utils import ApproximationFile
from models.features import get_feature_index
from models.exceptions import (
    FeatureSequencesNotFoundError,
    FeatureNotFoundError,
    SomeFeaturesNotFoundError,
)


def get_feature_sequences(
    organism,
    features,
    measurement_type="gene_expression",
):
    """Get the sequences of a list of features."""
    approx_path = get_atlas_path(organism)
    with ApproximationFile(approx_path) as db:
        if measurement_type not in db:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}",
                measurement_type=measurement_type,
            )
        if 'feature_sequences' not in db[measurement_type]:
            raise FeatureSequencesNotFoundError(
                "Feature sequences not found",
                organism=organism,
            )

        sequence_type = db[measurement_type]["feature_sequences"].attrs["type"]
        sequences = []
        features_not_found = []
        for fea in features:
            try:
                idx = get_feature_index(organism, fea.lower(), measurement_type)
            except FeatureNotFoundError as exc:
                features_not_found.append(fea)
                continue

            # If there are features not found, don't bother collecting sequences anymore
            if len(features_not_found):
                continue

            seq = db[measurement_type]["feature_sequences"]["sequences"].asstr()[idx]
            sequences.append(seq)

        if len(features_not_found):
            raise SomeFeaturesNotFoundError(
                f"Some features not found: {features}",
                features=features_not_found,
            )

    return features, sequences, sequence_type
