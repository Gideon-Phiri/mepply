# tests/test_routes.py

import pytest
from unittest.mock import patch, MagicMock
from app.routes.upload import app
from app.models.file_metadata import FileMetadata

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_set_storage(client, mocker):
    mocker.patch('app.routes.upload.verify_user', return_value="test_user_id")
    response = client.post(
        "/set-storage",
        json={"storage_type": "mongodb"},
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.json["message"] == "Primary storage set to mongodb"

def test_upload_file(client, mocker):
    mocker.patch('app.routes.upload.verify_user', return_value="test_user_id")
    mocker.patch('app.models.file_metadata.FileMetadata.get_file_metadata', return_value=None)
    mocker.patch('app.models.file_metadata.FileMetadata.get_primary_storage', return_value="mongodb")
    mocker.patch('app.services.file_manager.FileManager.upload_to_gridfs', return_value={
        "file_id": "test_file_id", "storage": "mongodb"
    })

    data = {'file': (MagicMock(), 'test.docx')}
    response = client.post(
        "/upload",
        headers={"Authorization": "Bearer test_token"},
        data=data,
        content_type='multipart/form-data'
    )

    assert response.status_code == 200
    assert response.json["message"] == "File uploaded successfully!"

def test_delete_file(client, mocker):
    mocker.patch('app.routes.upload.verify_user', return_value="test_user_id")
    mocker.patch('app.models.file_metadata.FileMetadata.get_file_metadata', return_value={
        "storage_type": "mongodb", "location": "test_file_id"
    })
    mocker.patch('app.services.file_manager.FileManager.delete_from_gridfs', return_value=True)

    response = client.delete(
        "/file",
        headers={"Authorization": "Bearer test_token"}
    )

    assert response.status_code == 200
    assert response.json["message"] == "File deleted successfully!"

