import pandas as pd

from models.paths import (
    get_interactions_path,
)



def get_interaction_partners(
    organism,
    features,
    measurement_type="gene_expression",
    ):
    
    if measurement_type != "gene_expression":
        raise MeasurementTypeNotFoundError(
            "Interactions are only available for gene expression at the moment.",
            measurement_type=measurement_type,
        )

    interaction_path = get_interactions_path(organism)
    table = pd.read_csv(interaction_path, sep='\t', compression='gzip')
    targets = []
    queries = []
    for feature in features:
        partners = list(table.loc[table['source_gene'] == feature, 'target_gene'].values)
        partners += list(table.loc[table['target_gene'] == feature, 'source_gene'].values)
        partners = list(set(partners))
        targets.extend(partners)
        queries.extend([feature] * len(partners))
    
    return {
        'targets': targets,
        'queries': queries,
    }
