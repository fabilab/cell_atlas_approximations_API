from flask import request
from flask_restful import abort

from models import (
    CellTypeNotFoundError,
    OrganismNotFoundError,
    OrganNotFoundError,
    FeatureNotFoundError,
    FeatureSequencesNotFoundError,
    SimilarityMethodError,
    MeasurementTypeNotFoundError,
    SomeFeaturesNotFoundError,
    TooManyFeaturesError,
    FeaturesNotPairedError,
    NeighborhoodNotFoundError,
)


class FeatureStringFormatError(Exception):
    def __init__(self, msg, features):
        self.features = features
        super().__init__(self, msg)


def required_parameters(*required_args):
    """Decorator that aborts if mandatory parameters are missing."""

    def inner(wrapped):
        """Just an inner layer used by Python to get rid of decorator parameters."""

        def func(*args_inner, **kwargs_inner):
            """Decorated function."""
            for arg in required_args:
                if request.args.get(arg, None) is None:
                    abort(
                        400,
                        message=f'The "{arg}" parameter is required.',
                        error={
                            "type": "missing_parameter",
                            "missing_parameter": arg,
                        },
                    )
            return wrapped(*args_inner, **kwargs_inner)

        return func

    return inner


def model_exceptions(func):
    """Closure that deals with model exceptions at the API level."""

    def inner(*args_inner, **kwargs_inner):
        try:
            return func(*args_inner, **kwargs_inner)
        except OrganismNotFoundError as exc:
            abort(
                400,
                message=f"Organism not found: {exc.organism}.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "organism",
                    "invalid_value": exc.organism,
                },
            )
        except OrganNotFoundError as exc:
            abort(
                400,
                message=f"Organ not found: {exc.organ}.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "organ",
                    "invalid_value": exc.organ,
                },
            )
        except CellTypeNotFoundError as exc:
            abort(
                400,
                message=f"Cell type not found: {exc.cell_type}.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "celltype",
                    "invalid_value": exc.cell_type,
                },
            )
        except FeatureNotFoundError as exc:
            abort(
                400,
                message=f"Feature could not be found: {exc.feature}.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "feature",
                    "invalid_value": exc.feature,
                },
            )
        except SomeFeaturesNotFoundError as exc:
            abort(
                400,
                message=f"Some features could not be found: {exc.features}.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "features",
                    "invalid_value": exc.features,
                },
            )
        except TooManyFeaturesError as exc:
            abort(
                400,
                message=f"Too many features requested.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "features",
                    "invalid_reason": "too_many",
                },
            )
        except MeasurementTypeNotFoundError as exc:
            abort(
                400,
                message=f"Measurement type not found: {exc.measurement_type}.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "measurement_type",
                    "invalid_value": exc.measurement_type,
                },
            )
        except SimilarityMethodError as exc:
            abort(
                400,
                message=f"Similarity method not supported: {exc.method}.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "method",
                    "invalid_value": exc.method,
                },
            )
        except FeatureSequencesNotFoundError as exc:
            abort(
                400,
                message=f"This organism has no feature sequences stored: {exc.organism}.",
                error={
                    "type": "missing_data",
                    "missing_data": "feature_sequences",
                },
            )
        except FeatureStringFormatError as exc:
            abort(
                400,
                message=f"Feature string not recognised: {exc.features}.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "features",
                    "invalid_value": exc.features,
                },
            )
        except NeighborhoodNotFoundError as exc:
            abort(
                400,
                message=f"This organism has no neighborhood stored: {exc.organism}.",
                error={
                    "type": "missing_data",
                    "missing_data": "neighborhood",
                },
            )
        except FeaturesNotPairedError as exc:
            abort(
                400,
                message="Features are not paired.",
                error={
                    "type": "invalid_parameter",
                    "features1": exc.features1,
                    "features2": exc.features2,
                },
            )
        except (ValueError, TypeError, KeyError) as exc:
            abort(
                400,
                message=f"Invalid value: {exc}.",
                error={
                    "type": "invalid_parameter",
                    "invalid_parameter": "value",
                    "invalid_value": str(exc),
                },
            )

    return inner
