from django.conf import settings
import pytest


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
