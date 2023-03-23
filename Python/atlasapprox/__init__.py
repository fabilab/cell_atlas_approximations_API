"""
Cell atlas approximations, Python API interface.
"""
import os
import requests
import pandas as pd
from typing import Sequence


__all__ = (
    "api_version",
    "BadRequestError",
    "API",
)


api_version = "v1"

baseurl = os.getenv(
    "ATLASAPPROX_BASEURL",
    f"http://api.atlasapprox.org/{api_version}/",
)


class BadRequestError(ValueError):
    """The API request was not formulated correctly."""
    pass


class API:
    """Main object used to access the atlas approximation API"""

    cache = {}

    def organisms(self):
        """Get a list of available organisms.

        Returns: A list of organisms.
        """
        if "organisms" not in self.cache:
            self._fetch_organisms()

        return self.cache["organisms"]

    def organs(self, organism: str):
        """Get a list of available organs.

        Args:
            organism: The organism to query.

        Returns: A list of organs.
        """
        if ("organs" not in self.cache) or (organism not in self.cache["organs"]):
            self._fetch_organs(organism)
        return self.cache["organs"][organism]

    def celltypes(self, organism: str, organ: str):
        """Get a list of celltypes in an organ and organism.

        Args:
            organism: The organism to query.
            organ: The organ to query.

        Return: A list of cell types.
        """
        if ("celltypes" not in self.cache) or (organ not in self.cache["celltypes"]):
            self._fetch_celltypes(organism, organ)
        return self.cache["celltypes"][(organism, organ)]

    def average(self, organism: str, organ: str, features: Sequence[str]):
        """Get average gene expression for specific features.

        Args:
            organism: The organism to query.
            organ: The organ to query.
            features: The features (e.g. genes) to query.

        Return: A pandas.DataFrame with the gene expression. Each column is
            a cell type, each row a feature.
        """
        response = requests.get(
            baseurl + "average",
            params={
                "organism": organism,
                "organ": organ,
                "features": ",".join(features),
            },
        )
        if response.ok:
            resjson = response.json()
            celltypes = self.celltypes(
                organism,
                organ,
            )
            features = resjson["features"]
            matrix = pd.DataFrame(
                resjson["average"],
                index=features,
                columns=celltypes,
            )
            return matrix
        else:
            raise BadRequestError(response.json()["message"])

    def fraction_detected(
        self,
        organism: str,
        organ: str,
        features: Sequence[str],
    ):
        """Get fraction of detected gene expression for specific features.

        Args:
            organism: The organism to query.
            organ: The organ to query.
            features: The features (e.g. genes) to query.

        Return: A pandas.DataFrame with the fraction expressing. Each column is
            a cell type, each row a feature.
        """
        response = requests.get(
            baseurl + "fraction_detected",
            params={
                "organism": organism,
                "organ": organ,
                "features": ",".join(features),
            },
        )
        if response.ok:
            resjson = response.json()
            celltypes = self.celltypes(
                organism,
                organ,
            )
            features = resjson["features"]
            matrix = pd.DataFrame(
                resjson["fraction_detected"],
                index=features,
                columns=celltypes,
            )
            return matrix
        else:
            raise BadRequestError(response.json()["message"])

    def markers(
        self,
        organism: str,
        organ: str,
        cell_type: str,
        number: int,
    ):
        """Get marker features (e.g. genes) for a cell type within an organ.

        Args:
            organism: The organism to query.
            organ: The organ to query.
            cell_type: The cell type to get markers for.
            number: The number of markers to look for. The actual number might
            be lower if not enough distinctive features were found.

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
            },
        )
        if response.ok:
            markers = response.json()["markers"]
            return markers
        else:
            raise BadRequestError(response.json()["message"])

    def _fetch_organisms(self):
        """Fetch organisms data"""
        response = requests.get(baseurl + "organisms")
        if response.ok:
            self.cache["organisms"] = response.json()["organisms"]
        else:
            raise BadRequestError(response.json()["message"])

    def _fetch_organs(self, organism: str):
        """Fetch organ data"""
        response = requests.get(
            baseurl + "organs",
            params={
                "organism": organism,
            },
        )
        if response.ok:
            if "organs" not in self.cache:
                self.cache["organs"] = {}
            self.cache["organs"][organism] = response.json()["organs"]
        else:
            raise BadRequestError(response.json()["message"])

    def _fetch_celltypes(self, organism: str, organ: str):
        """Fetch cell type data"""
        response = requests.get(
            baseurl + "celltypes",
            params={
                "organism": organism,
                "organ": organ,
            },
        )
        if response.ok:
            if "celltypes" not in self.cache:
                self.cache["celltypes"] = {}
            self.cache["celltypes"][(organism, organ)] = response.json()["celltypes"]
        else:
            raise BadRequestError(response.json()["message"])
