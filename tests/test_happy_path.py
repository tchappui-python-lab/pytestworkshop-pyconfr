import ftplib
import os
from pathlib import Path

from django.conf import settings
import pytest


@pytest.fixture
def file_url(file_on_storage, storage_service_instance):
    root_url = storage_service_instance["root_url"]
    fname = os.path.basename(file_on_storage)
    return root_url + fname + "/"


def ftp_checker(ip_address, port):
    try:
        ftplib.FTP(ip_address)
        return True
    except Exception:
        return False


@pytest.fixture
def storage_service_instance(docker_services):
    # remove all files in root dir
    root_dir = "/tmp/test-ftpdserver-pyconfr"
    Path(root_dir).mkdir(parents=True, exist_ok=True)
    for f in os.listdir(root_dir):
        os.remove(root_dir + "/" + f)

    docker_services.start("ftpd_server")
    docker_services.wait_for_service(
        "ftpd_server", 21, check_server=ftp_checker
    )

    return {"root_dir": root_dir, "root_url": "/api/v1/files/"}


@pytest.fixture
def file_on_storage(storage_service_instance):
    root_dir = storage_service_instance["root_dir"]
    fpath = os.path.join(root_dir, "file-to-test.txt")
    with open(fpath, "wb") as f:
        f.write(b"some foo bar content")

    return fpath


@pytest.fixture
def mocked_conf(monkeypatch):
    monkeypatch.setattr(
        settings,
        "DEFAULT_FILE_STORAGE",
        "storages.backends.ftp.FTPStorage",
        raising=False,
    )
    monkeypatch.setattr(
        settings,
        "FTP_STORAGE_LOCATION",
        "ftp://pyconfr:pyconfr@localhost:21",
        raising=False,
    )


def test_happy_path(mocked_conf, file_on_storage, file_url, client):
    response = client.get(file_url)

    assert response.status_code == 200

    with open(file_on_storage, "rb") as f:
        file_content = f.read()

        assert file_content == response.content
