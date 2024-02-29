# Web imports
from flask_restful import Resource


class DataSources(Resource):
    """Get list of organisms"""

    def get(self):
        """Get list of organisms"""
        return {
            "a_queenslandica": "Sebé-Pedrós et al 2018 (https://www.nature.com/articles/s41559-018-0575-6)",
            "a_thaliana": "Shahan et al 2022 (https://www.sciencedirect.com/science/article/pii/S1534580722000338)",
            "c_elegans": "Cao et al. 2017 (https://www.science.org/doi/10.1126/science.aam8940)",
            "c_hemisphaerica": "Chari et al. 2021 (https://www.science.org/doi/10.1126/sciadv.abh1683#sec-4)",
            "d_melanogaster": "Li et al. 2022 (https://doi.org/10.1126/science.abk2432)",
            "d_rerio": "Wagner et al. 2018 (https://www.science.org/doi/10.1126/science.aar4362)",
            "h_miamia": "Hulett et al. 2023 (https://www.nature.com/articles/s41467-023-38016-4)",
            "h_sapiens": "RNA: Tabula Sapiens (https://www.science.org/doi/10.1126/science.abl4896), ATAC: Zhang et al. Ren. A single-cell atlas of chromatin accessibility in the human genome (https://doi.org/10.1016/j.cell.2021.10.024).",
            "h_vulgaris": "Sieert et al 2019 (https://doi.org/10.1126/science.aav9314)",
            "i_pulchra": "Duruz et al. 2020 (https://academic.oup.com/mbe/article/38/5/1888/6045962)",
            "l_minuta": "Abramson et al. 2022 (https://doi.org/10.1093/plphys/kiab564)",
            "m_leidyi": "Sebé-Pedrós et al 2018 (https://www.nature.com/articles/s41559-018-0575-6)",
            "m_murinus": "Tabula Microcebus (https://www.biorxiv.org/content/10.1101/2021.12.12.469460v2)",
            "m_musculus": "Tabula Muris Senis 2020 (https://www.nature.com/articles/s41586-020-2496-1)",
            "n_vectensis": "Steger et al 2022 (https://doi.org/10.1016/j.celrep.2022.111370)",
            "s_lacustris": "Musser et al. 2021 (https://www.science.org/doi/10.1126/science.abj2949)",
            "s_mansoni": "Li et al. 2021 (https://www.nature.com/articles/s41467-020-20794-w)",
            "s_mediterranea": "Plass et al. 2018 (https://doi.org/10.1126/science.aaq1723)",
            "s_pistillata": "Levi et al. 2021 (https://www.sciencedirect.com/science/article/pii/S0092867421004402)",
            "t_adhaerens": "Sebé-Pedrós et al 2018 (https://www.nature.com/articles/s41559-018-0575-6)",
            "t_aestivum": "Zhang et al 2023 (https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-02908-x)",
            "x_laevis": "Liao et al. 2022 (https://www.nature.com/articles/s41467-022-31949-2)",
        }
