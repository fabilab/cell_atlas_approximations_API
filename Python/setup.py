"""
Setup script for atlasapprox Python package
"""
import pathlib
from setuptools import setup, find_packages


# version
version_file = pathlib.Path(__file__).parent / "VERSION"
with open(version_file) as f:
    version = f.read().rstrip('\n')


long_description = """[![Documentation Status](https://readthedocs.org/projects/atlasapprox/badge/?version=latest)](https://apidocs.atlasapprox.org/en/latest/?badge=latest)

Python interface to cell atlas approximations
=============================================
Cell atlases such as Tabula Muris and Tabula Sapiens are multi-organ single cell omics data sets describing entire organisms. A cell atlas approximation is a lossy and lightweight compression of a cell atlas that can be streamed via the internet.

This project enables biologists, doctors, and data scientist to quickly find answers for questions such as:

- *What is the expression of a specific gene in human lung?*
- *What are the marker genes of a specific cell type in mouse pancreas*?
- *What fraction of cells (of a specific type) express a gene of interest?*

In addition to this interface, these questions can be asked in R or in a language agnostic manner using the REST API. See the documentation for more info.


**Documentation**: https://atlasapprox.readthedocs.io/en/latest/python/index.html

**Development**: https://github.com/fabilab/cell_atlas_approximations_API
"""


setup(
    name="atlasapprox",
    url="https://apidocs.atlasapprox.org",
    description="Cell atlas approximations, Python API",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    author="Fabio Zanini",
    author_email="fabio.zanini@unsw.edu.au",
    version=version,
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
    ],
    python_requires=">=3.7",
    platforms="ALL",
    keywords=[
        "single cell",
        "cell atlas",
        "omics",
        "biology",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
