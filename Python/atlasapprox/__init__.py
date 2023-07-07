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


__all__ = (
    "api_version",
    "BadRequestError",
    "API",
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

Human:
  - RNA: Tabula Sapiens (https://www.science.org/doi/10.1126/science.abl4896)
  - ATAC: Zhang et al. 2021 (https://doi.org/10.1016/j.cell.2021.10.024)
Mouse: Tabula Muris Senis (https://www.nature.com/articles/s41586-020-2496-1)
Lemur: Tabula Microcebus (https://www.biorxiv.org/content/10.1101/2021.12.12.469460v2)
C elegans: Cao et al. 2017 (https://www.science.org/doi/10.1126/science.aam8940)
Zebrafish: Wagner et al. 2018 (https://www.science.org/doi/10.1126/science.aar4362)

To hide this message, set the environment variable ATLASAPPROX_HIDECREDITS to any
nonzero value, e.g.:

import os
os.environ["ATLASAPPROX_HIDECREDITS"] = "yes"
import atlasapprox

To propose a new atlas be added to the list of approximations, please contact
Fabio Zanini (fabio DOT zanini AT unsw DOT edu DOT au)."""
if show_credit:
    print(credit)


class API:
    """Main object used to access the atlas approximation API"""

    cache = {}

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
            _fetch_organs(self, organism)
        return self.cache["organs"][organism]

    def celltypes(
        self,
        organism: str,
        organ: str,
        measurement_type: str = "gene_expression",
    ):
        """Get a list of celltypes in an organ and organism.

        Args:
            organism: The organism to query.
            organ: The organ to query.
            measurement_type: The measurement type to query.

        Return: A list of cell types.
        """
        if ("celltypes" not in self.cache) or ((measurement_type, organism, organ) not in self.cache["celltypes"]):
            _fetch_celltypes(self, organism, organ, measurement_type)
        return self.cache["celltypes"][(measurement_type, organism, organ)]

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

    def celltypexorgan(
        self,
        organism: str,
        organs: Union[None, str] = None,
        measurement_type: str = "gene_expression",
    ):

        params = {
            "organism": organism,
            "measurement_type": measurement_type,
        }
        if organs is not None:
            params["organs"] = organs

        response = requests.get(
            baseurl + "celltypexorgan",
            params=params,
        )
        if not response.ok:
            raise BadRequestError(response.json()["message"])

        resp_result = response.json()
        result = pd.DataFrame(
            np.array(resp_result["detected"]).astype(bool),
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
