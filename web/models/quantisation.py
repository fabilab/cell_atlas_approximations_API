from models.paths import get_atlas_path
from models.utils import ApproximationFile
from models.exceptions import (
    MeasurementTypeNotFoundError,
)


quantisations = {}


def get_quantisation(organism, measurement_type):
    """Lazy cacher of data quantisations.

    NOTE: Data quantisation is sometimes needed to reduce file size. Even a simple 8-bit
    logarithmic quantisation of e.g. chromatin accessibility saves ~70% of space compared
    to 32-bit floats. The runtime overhead to undo the quantisation is minimal, even less
    if the quantisation vector (i.e. 256 float32 numbers) is lazily loaded into RAM via
    this function.
    """
    if (organism, measurement_type) not in quantisations:
        approx_path = get_atlas_path(organism)
        with ApproximationFile(approx_path) as db:
            if measurement_type not in db:
                raise MeasurementTypeNotFoundError(
                    f"Measurement type not found: {measurement_type}",
                    measurement_type=measurement_type,
                )
            if "quantisation" not in db[measurement_type]:
                raise KeyError(
                    f"No 'quantisation' key found for {organism}, {measurement_type}."
                )
            quantisations[(organism, measurement_type)] = db[measurement_type][
                "quantisation"
            ][:]
    return quantisations[(organism, measurement_type)]



