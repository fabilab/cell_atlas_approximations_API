def clean_feature_string(features, organism=None):
    """Clean feature string and split into a list."""
    features = features.replace('"', "").replace("'", "").replace(" ", "")

    features = features.split(",")

    # Correct capitalization based on species
    if organism == "m_musculus":
        features = [fea.capitalize() for fea in features]
    elif organism == "h_sapiens":
        features = [fea.upper() for fea in features]

    return features
