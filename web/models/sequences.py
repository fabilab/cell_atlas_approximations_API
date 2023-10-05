"""Feature sequences (e.g. genes, transcripts, peaks)"""
from config import configuration as config
from models.paths import get_atlas_path
from models.utils import ApproximationFile
from models.features import get_feature_index
from models.exceptions import (
    FeatureSequencesNotFoundError,
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
                f"Measurement type not found: {measurement_type}"
            )
        if 'feature_sequences' not in db[measurement_type]:
            raise FeatureSequencesNotFoundError(
                "Feature sequences not found",
            )

        sequence_type = db[measurement_type]["feature_sequences"].attrs["type"]
        sequences = []
        for fea in features:
            idx = get_feature_index(
                organism,
                fea.lower(),
                measurement_type=measurement_type,
            )
            seq = db[measurement_type]["feature_sequences"]["sequences"].asstr()[idx]
            sequences.append(seq)

    return features, sequences, sequence_type
