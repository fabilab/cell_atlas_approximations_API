class OrganismNotFoundError(KeyError):
    pass


class OrganNotFoundError(KeyError):
    pass


class MeasurementTypeNotFoundError(KeyError):
    pass


class FeatureNotFoundError(KeyError):
    def __init__(self, msg, feature):
        self.feature = feature
        super().__init__(self, msg)


class SomeFeaturesNotFoundError(KeyError):
    def __init__(self, msg, features):
        self.features = features
        super().__init__(self, msg)


class FeatureSequencesNotFoundError(KeyError):
    pass


class TooManyFeaturesError(ValueError):
    pass


class CellTypeNotFoundError(KeyError):
    pass


class SimilarityMethodError(NotImplementedError):
    pass


class OrganCellTypeError(KeyError):
    pass

