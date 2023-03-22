"""
Setup script for atlasapprox Python package
"""
import pathlib
from setuptools import setup, find_packages


# version
version_file = pathlib.Path(__file__).parent / "VERSION"
with open(version_file) as f:
    version = f.read().rstrip('\n')


setup(
    name="atlasapprox",
    version=version,
    packages=find_packages(),
)
