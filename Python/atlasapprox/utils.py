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
