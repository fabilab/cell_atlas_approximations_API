import requests

from atlasapprox.exceptions import BadRequestError


def _fetch_organisms(api, measurement_type: str):
    """Fetch organisms data"""
    response = requests.get(
        api.baseurl + "organisms",
        params={
            "measurement_type": measurement_type,
        },
    )
    if response.ok:
        if "organisms" not in api.cache:
            api.cache["organisms"] = {}
        api.cache["organisms"][measurement_type] = response.json()["organisms"]
    else:
        raise BadRequestError(response.json()["message"])


def _fetch_organs(api, organism: str, measurement_type: str):
    """Fetch organ data"""
    response = requests.get(
        api.baseurl + "organs",
        params={
            "organism": organism,
            "measurement_type": measurement_type,
        },
    )
    if response.ok:
        if "organs" not in api.cache:
            api.cache["organs"] = {}
        api.cache["organs"][(measurement_type, organism)] = response.json()["organs"]
    else:
        raise BadRequestError(response.json()["message"])


def _fetch_celltypes(api, organism: str, organ: str, measurement_type: str, include_abundance: bool):
    """Fetch cell type data"""
    response = requests.get(
        api.baseurl + "celltypes",
        params={
            "organism": organism,
            "organ": organ,
            "include_abundance": include_abundance,
            "measurement_type": measurement_type,
        },
    )
    if response.ok:
        if "celltypes" not in api.cache:
            api.cache["celltypes"] = {}
        if include_abundance:
            res_dict = response.json()
            res = {
                'celltypes': res_dict['celltypes'],
                'abundance': res_dict['abundance'],
            }
            api.cache["celltypes"][(measurement_type, organism, organ, include_abundance)] = res
        else:
            api.cache["celltypes"][(measurement_type, organ, include_abundance)] = response.json()["celltypes"]
    else:
        raise BadRequestError(response.json()["message"])
