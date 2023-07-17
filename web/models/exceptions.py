class OrganismNotFoundError(KeyError):
    pass


class OrganNotFoundError(KeyError):
    pass


class MeasurementTypeNotFoundError(KeyError):
    pass


class FeatureNotFoundError(KeyError):
    pass


class TooManyFeaturesError(ValueError):
    pass


class CellTypeNotFoundError(KeyError):
    pass


class SimilarityMethodError(NotImplementedError):
    pass


class OrganCellTypeError(KeyError):
    pass

