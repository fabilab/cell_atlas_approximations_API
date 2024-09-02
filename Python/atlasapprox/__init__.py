"""
Cell atlas approximations, Python API interface.
"""
import os
import requests
import numpy as np
import pandas as pd
from typing import Sequence, Union

from atlasapprox.exceptions import BadRequestError
from atlasapprox.utils import (
   _fetch_organisms,
   _fetch_organs,
   _fetch_celltypes,
)

__version__ = "0.2.2"

__all__ = (
    "api_version",
    "BadRequestError",
    "API",
    __version__,
)


api_version = "v1"

baseurl = os.getenv(
    "ATLASAPPROX_BASEURL",
    "http://api.atlasapprox.org",
)
baseurl = baseurl.rstrip("/") + "/"
baseurl += f"{api_version}/"

show_credit = os.getenv("ATLASAPPROX_HIDECREDITS") is None
credit = """Data sources for the approximations:

Animals:
- Homo sapiens (human):
  - RNA: Tabula Sapiens (https://www.science.org/doi/10.1126/science.abl4896)
  - ATAC: Zhang et al. 2021 (https://doi.org/10.1016/j.cell.2021.10.024)
- Mus musculus (mouse): Tabula Muris Senis (https://www.nature.com/articles/s41586-020-2496-1)
- Microcebus murinus (mouse lemur): Tabula Microcebus (https://www.biorxiv.org/content/10.1101/2021.12.12.469460v2)
- Caenorhabditis elegans: Cao et al. 2017 (https://www.science.org/doi/10.1126/science.aam8940)
- Crassostrea gigas: Piovani et al. 2023 (https://doi.org/10.1126/sciadv.adg6034)
- Danio rerio (zebrafish): Wagner et al. 2018 (https://www.science.org/doi/10.1126/science.aar4362)
- Clytia hemisphaerica: Chari et al. 2021 (https://www.science.org/doi/10.1126/sciadv.abh1683#sec-4)
- Drosophila melanogaster (fruitfly): Li et al. 2022 (https://doi.org/10.1126/science.abk2432
- Hofstenia miamia: Hulett et al. 2023 (https://www.nature.com/articles/s41467-023-38016-4)
- Isodiametra pulchra: Duruz et al. 2020 (https://academic.oup.com/mbe/article/38/5/1888/6045962)
- Mnemiopsis leidyi: Sebé-Pedrós et al 2018 (https://www.nature.com/articles/s41559-018-0575-6)
- Nematostella vectensis: Steger et al 2022 (https://doi.org/10.1016/j.celrep.2022.111370)
- Prostheceraeus crozieri: Piovani et al. 2023 (https://doi.org/10.1126/sciadv.adg6034)
- Platynereis dumerilii: Achim et al 2017 (https://academic.oup.com/mbe/article/35/5/1047/4823215)
- Strongylocentrotus purpuratus (sea urchin): Paganos et al. 2021 (https://doi.org/10.7554/eLife.70416)
- Spongilla lacustris: Musser et al. 2021 (https://www.science.org/doi/10.1126/science.abj2949)
- Schistosoma mansoni: Li et al. 2021 (https://www.nature.com/articles/s41467-020-20794-w)
- Schmidtea mediterranea: Plass et al. 2018 (https://doi.org/10.1126/science.aaq1723)
- Stylophora pistillata: Levi et al. 2021 (https://www.sciencedirect.com/science/article/pii/S0092867421004402)
- Trichoplax adhaerens: Sebé-Pedrós et al 2018 (https://www.nature.com/articles/s41559-018-0575-6)
- Triticum aestivum (wheat): Zhang et al 2023 (https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-02908-x)
- Xenopus laevis: Liao et al. 2022 (https://www.nature.com/articles/s41467-022-31949-2)

Plants:
- Arabidopsis thaliana: Shahan et al 2022 (https://www.sciencedirect.com/science/article/pii/S1534580722000338), Xu et al. 2024 (https://www.biorxiv.org/content/10.1101/2024.03.04.583414v1)
- Lemna minuta: Abramson et al. 2022 (https://doi.org/10.1093/plphys/kiab564)

To hide this message, set the environment variable ATLASAPPROX_HIDECREDITS to any
nonzero value, e.g.:

import os
os.environ["ATLASAPPROX_HIDECREDITS"] = "yes"
import atlasapprox

To propose a new atlas be added to the list of approximations, please contact
Fabio Zanini (fabio DOT zanini AT unsw DOT edu DOT au)."""
if show_credit:
    print(credit)
    show_credit = False


class API:
    """Main object used to access the atlas approximation API"""

    cache = {}

    def __init__(self, url=None):
        """Create an instance of the atlasapprox API.

        """
        self.baseurl = url if url is not None else baseurl

    def measurement_types(self):
        """Get a list of measurement types.

        Returns: A list of measurement types.
        """
        response = requests.get(baseurl + "measurement_types")
        if response.ok:
            return response.json()
        raise BadRequestError(response.json()["message"])

    def organisms(self, measurement_type: str = "gene_expression"):
        """Get a list of available organisms.

        Args:
            measurement_type: The measurement type to query.

        Returns: A list of organisms.
        """
        if "organisms" not in self.cache:
            _fetch_organisms(self, measurement_type)

        return self.cache["organisms"]

    def organs(
        self,
        organism: str,
        measurement_type: str = "gene_expression",
    ):
        """Get a list of available organs.

        Args:
            organism: The organism to query.
            measurement_type: The measurement type to query.

        Returns: A list of organs.
        """
        if ("organs" not in self.cache) or (organism not in self.cache["organs"]):
            _fetch_organs(self, organism, measurement_type)
        return self.cache["organs"][organism]

    def celltypes(
        self,
        organism: str,
        organ: str,
        measurement_type: str = "gene_expression",
        include_abundance: bool = False,
    ):
        """Get a list of celltypes in an organ and organism.

        Args:
            organism: The organism to query.
            organ: The organ to query.
            measurement_type: The measurement type to query.
            include_abundance: Whether to include abundance in the result (optional).

        Return: A list of cell types.
        """
        if ("celltypes" not in self.cache) or ((measurement_type, organism, organ, include_abundance) not in self.cache["celltypes"]):
            _fetch_celltypes(self, organism, organ, measurement_type, include_abundance)
        return self.cache["celltypes"][(measurement_type, organism, organ, include_abundance)]

    def average(
        self,
        organism: str,
        organ: str,
        features: Sequence[str],
        measurement_type: str = "gene_expression",
    ):
        """Get average gene expression for specific features.

        Args:
            organism: The organism to query.
            organ: The organ to query.
            features: The features (e.g. genes) to query.
            measurement_type: The measurement type to query.

        Return: A pandas.DataFrame with the gene expression. Each column is
            a cell type, each row a feature. The unit of measurement, or
            normalisation, is counts per ten thousand (cptt).
        """
        response = requests.get(
            baseurl + "average",
            params={
                "organism": organism,
                "organ": organ,
                "features": ",".join(features),
                "measurement_type": measurement_type,
            },
        )
        if response.ok:
            resjson = response.json()
            celltypes = resjson["celltypes"]
            features = resjson["features"]
            matrix = pd.DataFrame(
                resjson["average"],
                index=features,
                columns=celltypes,
            )
            return matrix
        raise BadRequestError(response.json()["message"])

    def fraction_detected(
        self,
        organism: str,
        organ: str,
        features: Sequence[str],
        measurement_type: str = "gene_expression",
    ):
        """Get fraction of detected gene expression for specific features.

        Args:
            organism: The organism to query.
            organ: The organ to query.
            features: The features (e.g. genes) to query.
            measurement_type: The measurement type to query.

        Return: A pandas.DataFrame with the fraction expressing. Each column is
            a cell type, each row a feature.
        """
        response = requests.get(
            baseurl + "fraction_detected",
            params={
                "organism": organism,
                "organ": organ,
                "features": ",".join(features),
                "measurement_type": measurement_type,
            },
        )
        if response.ok:
            resjson = response.json()
            celltypes = resjson["celltypes"]
            features = resjson["features"]
            matrix = pd.DataFrame(
                resjson["fraction_detected"],
                index=features,
                columns=celltypes,
            )
            return matrix
        raise BadRequestError(response.json()["message"])

    def dotplot(
        self,
        organism: str,
        organ: str,
        features: Sequence[str],
        measurement_type: str = "gene_expression",
    ):
        """Get average and fraction detected for specific features.

        Args:
            organism: The organism to query.
            organ: The organ to query.
            features: The features (e.g. genes) to query.
            measurement_type: The measurement type to query.

        Return: A pandas.DataFrame with the fraction expressing. Each column is
            a cell type, each row a feature.
        """
        response = requests.get(
            baseurl + "fraction_detected",
            params={
                "organism": organism,
                "organ": organ,
                "features": ",".join(features),
                "measurement_type": measurement_type,
            },
        )
        if response.ok:
            resjson = response.json()
            celltypes = resjson["celltypes"]
            features = resjson["features"]
            matrix = pd.DataFrame(
                resjson["fraction_detected"],
                index=features,
                columns=celltypes,
            )
            return matrix
        raise BadRequestError(response.json()["message"])

    def features(
        self,
        organism: str,
        measurement_type: str = "gene_expression",
    ):
        """Get names of features (e.g. genes) in this organism and measurement type.

        Args:
            organism: The organism to query.
            measurement_type: The measurement type to query.
        Return: A pandas.Index with the features.
        """
        response = requests.get(
            baseurl + "features",
            params={
                "organism": organism,
                "measurement_type": measurement_type,
            },
        )
        if not response.ok:
            raise BadRequestError(response.json()["message"])

        resjson = response.json()
        features = resjson["features"]
        result = pd.Index(
            features,
            name='features',
        )
        return result

    def sequences(
        self,
        organism: str,
        features: Sequence[str],
        measurement_type: str = "gene_expression",
    ):
        """Return the sequences of the requested features and their type.

        Args:
            organism: The organism to query.
            features: The features (e.g. genes) to query.
            measurement_type: The measurement type to query.
        Return: A dictionary with two keys, "type" indicating what kind of sequences
            they are, and "sequences" with a list of the sequences in the same order.
            If a feature sequence is not found, it is set to None.
        """
        response = requests.get(
            baseurl + "sequences",
            params={
                "organism": organism,
                "features": ",".join(features),
                "measurement_type": measurement_type,
            },
        )
        if not response.ok:
            raise BadRequestError(response.json()["message"])

        resjson = response.json()
        sequences = resjson["sequences"]
        seqtype = resjson["type"]
        for i, seq in enumerate(sequences):
            if seq == "":
                sequences[i] = None

        return {
            "type": seqtype,
            "sequences": sequences,
        }

    def neighborhood(
        self,
        organism: str,
        organ: str,
        features: Union[None, Sequence[str]] = None,
        include_embeding: bool = True,
        measurement_type: str = "gene_expression",
    ):
        """Neighborhood or cell state information.

        Args:
            organism: The organism to query.
            features: The features (e.g. genes) to query. This argument is optional.
            measurement_type: The measurement type to query.
        Return: A dict with a few key/value pairs:
            TODO
        """
        params = {
            "organism": organism,
            "measurement_type": measurement_type,
            "include_embedding": include_embedding,
        }
        if (features is not None) and len(features):
            params["features"] = ",".join(features),

        response = requests.get(
            baseurl + "neighborhood",
            params=params,
        )
        if not response.ok:
            raise BadRequestError(response.json()["message"])

        resjson = response.json()
        ncells = resjson["ncells"]
        celltypes = resjson["celltypes"]
        ncells = pd.DataFrame(
            ncells,
            index=celltypes,
        )
        res = {
            "ncells": ncells,
        }
        if (features is not None) and len(features):
            res["average"] = pd.DataFrame(
                resjson["average"],
                index=celltypes,
                columns=features,
            )
            if "fraction_detected" in resjson:
                res["fraction_detected"] = pd.DataFrame(
                    resjson["fraction_detected"],
                    index=celltypes,
                    columns=features,
                )

        if include_embedding:
            res["centroids"] = pd.DataFrame(
                resjson["centroids"],
                columns=["embedding 1", "embedding 2"],
            )
            res["boundaries"] = []
            for bound in resjson["boundaries"]:
                bound_new = pd.DataFrame(
                    bound,
                    columns=["embedding 1", "embedding 2"],
                )
                res["boundaries"].append(bound_new)

        return res

    def similar_features(
        self,
        organism: str,
        organ: str,
        feature: str,
        number: int,
        method: str = "correlation",
        measurement_type: str = "gene_expression",
    ):
        """Get features most similar to a focal one.

        Args:
            organism: The organism to query.
            organ: The organ to query.
            feature: The feature (e.g. gene) to look for similar featues to.
            number: The number of similar features to return.
            method: The method used to compute similarity between features. The
                following methods are available:
                - correlation (default): Pearson correlation of the fraction_detected
                - cosine: Cosine similarity/distance of the fraction_detected
                - euclidean: Euclidean distance of average measurement (e.g. expression)
                - manhattan: Taxicab/Manhattan/L1 distance of average measurement
                - log-euclidean: Log the average measurement with a pseudocount
                  of 0.001, then compute euclidean distance. This tends to
                  highlight sparsely measured features
            measurement_type: The measurement type to query.

        Return: A pandas.Series with the similar features and their distance
            from the focal feature according to the chosen method.
        """
        response = requests.get(
            baseurl + "similar_features",
            params={
                "organism": organism,
                "organ": organ,
                "feature": feature,
                "number": number,
                "method": method,
                "measurement_type": measurement_type,
            },
        )
        if not response.ok:
            raise BadRequestError(response.json()["message"])

        resjson = response.json()
        similar_features = resjson["similar_features"]
        distances = resjson["distances"]
        result = pd.Series(
            distances,
            index=similar_features,
        )
        return result

    def similar_celltypes(
        self,
        organism: str,
        organ: str,
        celltype: str,
        number: int,
        method: str = "correlation",
        measurement_type: str = "gene_expression",
    ):
        """Get cell types most similar to a focal one, across organs.

        Args:
            organism: The organism to query.
            organ: The organ to query. This and the next argument are to be
                interpreted together as fully specifying a cell type of interest.
            celltype: The cell type to look for similar featues to.
            number: The number of similar cell types to return.
            method: The method used to compute similarity between features. The
                following methods are available:
                - correlation (default): Pearson correlation of the fraction_detected
                - cosine: Cosine similarity/distance of the fraction_detected
                - euclidean: Euclidean distance of average measurement (e.g. expression)
                - manhattan: Taxicab/Manhattan/L1 distance of average measurement
                - log-euclidean: Log the average measurement with a pseudocount
                  of 0.001, then compute euclidean distance. This tends to
                  highlight sparsely measured features
            measurement_type: The measurement type to query.

        Return: A pandas.Series with the similar (organ, celltype) and their
            distance from the focal feature according to the chosen method.
        """
        response = requests.get(
            baseurl + "similar_celltypes",
            params={
                "organism": organism,
                "organ": organ,
                "celltype": celltype,
                "number": number,
                "method": method,
                "measurement_type": measurement_type,
            },
        )
        if not response.ok:
            raise BadRequestError(response.json()["message"])

        resjson = response.json()
        similar_organs = resjson["similar_organs"]
        similar_celltypes = resjson["similar_celltypes"]
        distances = resjson["distances"]
        index = pd.MultiIndex.from_arrays(
            [similar_organs, similar_celltypes],
            names=['organ', 'cell type'],
        )
        result = pd.Series(
            distances,
            index=index,
        )
        return result

    def markers(
        self,
        organism: str,
        organ: str,
        cell_type: str,
        number: int,
        measurement_type: str = "gene_expression",
    ):
        """Get marker features (e.g. genes) for a cell type within an organ.

        Args:
            organism: The organism to query.
            organ: The organ to query.
            cell_type: The cell type to get markers for.
            number: The number of markers to look for. The actual number might
                be lower if not enough distinctive features were found.
            measurement_type: The measurement type to query.

        Returns: A list of markers for the specified cell type in that organ.
            The number of markers might be less than requested if the cell type
            lacks distinctive features.
        """
        response = requests.get(
            baseurl + "markers",
            params={
                "organism": organism,
                "organ": organ,
                "celltype": cell_type,
                "number": number,
                "measurement_type": measurement_type,
            },
        )
        if response.ok:
            return response.json()["markers"]
        raise BadRequestError(response.json()["message"])

    def highest_measurement(
        self,
        organism: str,
        feature: str,
        number: int,
        measurement_type: str = "gene_expression",
    ):
        """Get the highest measurements by cell type across an organism.

        Args:
            organism: The organism to query.
            number: The number of cell types to list. The actual number might
                be lower if not enough cell types were found.
            measurement_type: The measurement type to query.

        Returns: A pandas.Series with a multi-index containing cell type and
            organ and values corresponding to the average measurement (e.g.
            gene expression) for that feature in that cell type and organ.
        """
        response = requests.get(
            baseurl + "highest_measurement",
            params={
                "organism": organism,
                "feature": feature,
                "number": number,
                "measurement_type": measurement_type,
            },
        )
        if not response.ok:
            raise BadRequestError(response.json()["message"])

        resp_result = response.json()
        result = pd.DataFrame(
            {
                "celltype": resp_result["celltypes"],
                "organ": resp_result["organs"],
                "average": resp_result["average"],
            }
        )
        result.set_index(["celltype", "organ"], inplace=True)
        return result["average"]

    def celltype_location(
        self,
        organism: str,
        cell_type: str,
        measurement_type: str = "gene_expression",
    ):
        """Get the organs/locations where a cell type is found.

        Args:
            organism: The organism to query.
            cell_type: The cell type to get markers for.
            measurement_type: The measurement type to query.

        Returns: A list of organs where that cell type is found.
        """
        response = requests.get(
            baseurl + "celltype_location",
            params={
                "organism": organism,
                "celltype": cell_type,
                "measurement_type": measurement_type,
            },
        )
        if not response.ok:
            raise BadRequestError(response.json()["message"])
        return response.json()["organs"]

    def celltypexorgan(
        self,
        organism: str,
        organs: Union[None, str] = None,
        measurement_type: str = "gene_expression",
        boolean=False,
    ):
        """Get the table of cell types x organ across a whole organism.

        Args:
            organism: The organism to query.
            organs (optional): If None, cover all organs from the chosen organism. If a list
                of organs, limit the table to those organs.
            measurement_type: The measurement type to query.
            boolean: If True, return a presence/absence matrix for each cell type in each
                organ. If False (default), return the number of sampled cells/nuclei for
                each cell type in each organ.

        Returns: A pandas.DataFrame with the presence/absence or number of sampled cells/nuclei
            for each cell type (index) in each organ (columns).
        """

        params = {
            "organism": organism,
            "measurement_type": measurement_type,
            "boolean": bool(boolean),
        }
        if organs is not None:
            params["organs"] = organs

        response = requests.get(
            baseurl + "celltypexorgan",
            params=params,
        )
        if not response.ok:
            raise BadRequestError(response.json()["message"])

        dtype = bool if boolean else int
        resp_result = response.json()
        result = pd.DataFrame(
            np.array(resp_result["detected"]).astype(dtype),
            columns=pd.Index(resp_result["organs"], name="organs"),
            index=pd.Index(resp_result["celltypes"], name="cell types"),
        )
        return result

    def data_sources(self):
        """List the cell atlases used as data sources."""
        response = requests.get(baseurl + "data_sources")
        if response.ok:
            return response.json()
        raise BadRequestError(response.json()["message"])
