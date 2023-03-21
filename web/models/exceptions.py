class OrganismNotFoundError(KeyError):
    pass


class MeasurementTypeNotFoundError(KeyError):
    pass


class FeatureNotFoundError(KeyError):
    pass


class TooManyFeaturesError(ValueError):
    pass


class CellTypeNotFoundError(KeyError):
    pass
