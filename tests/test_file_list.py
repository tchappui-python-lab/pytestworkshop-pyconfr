def test_empty_response(client, storage_service_instance):
    url = storage_service_instance["root_url"]
    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == {"results": []}


def test_nonempty_response(client, storage_service_instance, file_on_storage):
    url = storage_service_instance["root_url"]
    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == {"results": [{"name": "file-to-test.txt"}]}
