import numpy as np
import pandas as pd
import h5py
import hdf5plugin

from models.paths import get_protein_embeddings_path


def _get_prost_embeddings(organism=None, features=None):
    """Get embeddings for everything or specific organisms/features."""
    fn_embeddings = get_protein_embeddings_path()
    with h5py.File(fn_embeddings) as h5:
        if organism is None:
            raise NotImplementedError("Merging of all embeddings not implemented yet.")

        if organism not in h5:
            raise OrganismNotFoundError(
                f"Organism not found: {organism}",
                organism=organism,
            )

        group = h5[organism]
        index = group['features'].asstr()[:]
        if features is None:
            embeddings = group['embeddings'][:, :]
            return {
                'features': index,
                'embeddings': embeddings.astype('f4') / 256.0,
            }

        # Increasing, numerical indices for the selected features
        idx_features = pd.Series(index, index=np.arange(len(index)))
        idx_features = idx_features[idx_features.isin(features)].index
        if len(idx_features) == 0:
            return {
                'features': [],
                'embeddings': [],
            }

        features_found = index[idx_features]
        embeddings_found = group['embeddings'][idx_features, :]
        return {
            'features': features_found,
            'embeddings': embeddings_found.astype('f4') / 256.0,
        }


def get_homologs(
    query_organism,
    query_features,
    target_organism,
    max_distance=60,
    max_after_first=8,
):
    """Get homologous features across species using PROST protein embeddings."""
    emb_queries = _get_prost_embeddings(organism=query_organism, features=query_features)
    emb_target = _get_prost_embeddings(organism=target_organism)

    matches = []
    for feature, embedding in zip(emb_queries['features'], emb_queries['embeddings']):
        # PROST requires L1 distance
        dis = np.abs((emb_target['embeddings'] - embedding)).sum(axis=1)

        # Identify all features within distance
        idx_homologs = (dis < max_distance).nonzero()[0]
        if len(idx_homologs) == 0:
            continue
        homologs = emb_target['features'][idx_homologs]
        dis_homologs = dis[idx_homologs]

        # Restrict to closest and similia
        min_distance = dis_homologs.min()
        idx_homologs = dis_homologs <= max_after_first + min_distance
        homologs = homologs[idx_homologs]
        dis_homologs = dis_homologs[idx_homologs]

        # Append to matches
        for homolog, dis_homolog in zip(homologs, dis_homologs):
            matches.append([feature, homolog, float(dis_homolog)])
    return matches

