def clean_feature_string(features):
    """Clean feature string and split into a list."""
    features = features.replace('"', "").replace("'", "").replace(" ", "").split(",")
    return features
