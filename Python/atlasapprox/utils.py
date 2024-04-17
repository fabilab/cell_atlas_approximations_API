def _fetch_organisms(self):
    """Fetch organisms data"""
    response = requests.get(
        baseurl + "organisms",
        params={
            "measurement_type": measurement_type,
        },
    )
    if response.ok:
        if "organisms" not in self.cache:
            self.cache["organisms"] = {}
        self.cache["organisms"][measurement_type] = response.json()["organisms"]
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
        self.cache["organs"][(measurement_type, organism)] = response.json()["organs"]
    else:
        raise BadRequestError(response.json()["message"])

def _fetch_celltypes(self, organism: str, organ: str, measurement_type: str, include_abundance: bool):
    """Fetch cell type data"""
    response = requests.get(
        baseurl + "celltypes",
        params={
            "organism": organism,
            "organ": organ,
            "include_abundance": include_abundance,
            "measurement_type": measurement_type,
        },
    )
    if response.ok:
        if "celltypes" not in self.cache:
            self.cache["celltypes"] = {}
        if include_abundance:
            res_dict = response.json()
            res = {
                'celltypes': res_dict['celltypes'],
                'abundance': res_dict['abundance'],
            }
            self.cache["celltypes"][(measurement_type, organism, organ, include_abundance)] = res
        else:
            self.cache["celltypes"][(measurement_type, organ, include_abundance)] = response.json()["celltypes"]
    else:
        raise BadRequestError(response.json()["message"])
