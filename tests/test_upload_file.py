def test_upload_file(client, storage_service_instance, localfile):
    url = storage_service_instance["root_url"]
    response = client.post(url, {"upload.txt": localfile})

    assert response.status_code == 201
    assert response.json() == [{"name": "upload.txt"}]
