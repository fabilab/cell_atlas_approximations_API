import os
import pytest
import pathlib
import subprocess as sp

server_prefix = "http://127.0.0.1:5000/"
api_version = "v1"


@pytest.fixture(scope="session")
def webserver():
    #  TODO
    cwd = os.getcwd()
    test_script_folder = pathlib.Path(__file__).parent.parent
    try:
        os.chdir(test_script_folder)
        test_path = test_script_folder / "test.sh"
        sp.run(str(test_path), shell=True, check=True)

        yield

    finally:
        os.chdir(cwd)


@pytest.fixture(scope="session")
def host():
    return server_prefix+api_version
