# Web imports
from flask_restful import Resource


class DataSources(Resource):
    """Get list of organisms"""

    def get(self):
        """Get list of organisms"""
        return {
            "h_sapiens": "Tabula Sapiens (https://www.science.org/doi/10.1126/science.abl4896)",
            "m_musculus": "Tabula Muris Senis (https://www.nature.com/articles/s41586-020-2496-1)",
            "m_myoxinus": "Tabula Microcebus (https://www.biorxiv.org/content/10.1101/2021.12.12.469460v2)",
            "c_elegans": "Cao et al. 2017 (https://www.science.org/doi/10.1126/science.aam8940)",
            "d_rerio": "Wagner et al. 2018 (https://www.science.org/doi/10.1126/science.aar4362)",
            "s_lacustris": "Musser et al. 2021 (https://www.science.org/doi/10.1126/science.abj2949)",
            "a_queenslandica": "Sebé-Pedrós et al 2018 (https://www.nature.com/articles/s41559-018-0575-6)",
            "m_leidyi": "Sebé-Pedrós et al 2018 (https://www.nature.com/articles/s41559-018-0575-6)",
            "t_adhaerens": "Sebé-Pedrós et al 2018 (https://www.nature.com/articles/s41559-018-0575-6)",
        }
