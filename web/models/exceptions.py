class OrganismNotFoundError(KeyError):
    def __init__(self, msg, organism):
        self.organism = organism
        super().__init__(self, msg)


class OrganNotFoundError(KeyError):
    def __init__(self, msg, organ):
        self.organ = organ
        super().__init__(self, msg)


class OneOrganError(Exception):
    pass


class MeasurementTypeNotFoundError(KeyError):
    def __init__(self, msg, measurement_type):
        self.measurement_type = measurement_type
        super().__init__(self, msg)


class FeatureNotFoundError(KeyError):
    def __init__(self, msg, feature):
        self.feature = feature
        super().__init__(self, msg)


class SomeFeaturesNotFoundError(KeyError):
    def __init__(self, msg, features):
        self.features = features
        super().__init__(self, msg)


class FeatureSequencesNotFoundError(KeyError):
    def __init__(self, msg, organism):
        self.organism = organism
        super().__init__(self, msg)


class TooManyFeaturesError(ValueError):
    pass


class CellTypeNotFoundError(KeyError):
    def __init__(self, msg, cell_type):
        self.cell_type = cell_type
        super().__init__(self, msg)


class SimilarityMethodError(NotImplementedError):
    def __init__(self, msg, method):
        self.method = method
        super().__init__(self, msg)


class OrganCellTypeError(KeyError):
    pass


class NeighborhoodNotFoundError(KeyError):
    def __init__(self, organism, organ):
        self.organism = organism
        self.organ = organ
        msg = f"Neighborhood not found: {organism} {organ}"
        super().__init__(self, msg)
