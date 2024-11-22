# tests/test_upload_routes.py

import pytest
from unittest.mock import patch, MagicMock
from app.routes.upload import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_set_storage(client, mocker):
    # Mock verify_user to simulate user verification
    mocker.patch('app.routes.upload.verify_user', return_value="test_user_id")

    response = client.post(
        "/set-storage",
        json={"storage_type": "dropbox"},
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.json["message"] == "Primary storage set to dropbox"

def test_upload_file(client, mocker):
    # Mock verify_user and storage methods
    mocker.patch('app.routes.upload.verify_user', return_value="test_user_id")
    mocker.patch('app.models.file_metadata.FileMetadata.get_file_metadata', return_value=None)
    mocker.patch('app.models.file_metadata.FileMetadata.get_primary_storage', return_value="dropbox")
    mocker.patch('app.services.file_manager.FileManager.upload_to_dropbox', return_value={
        "link": "https://www.dropbox.com/s/test_link", "storage": "dropbox"
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
    assert response.json["storage"]["storage"] == "dropbox"

def test_upload_file_already_exists(client, mocker):
    # Mock verify_user and return existing file metadata
    mocker.patch('app.routes.upload.verify_user', return_value="test_user_id")
    mocker.patch('app.models.file_metadata.FileMetadata.get_file_metadata', return_value={"filename": "test.docx"})

    data = {'file': (MagicMock(), 'test.docx')}
    response = client.post(
        "/upload",
        headers={"Authorization": "Bearer test_token"},
        data=data,
        content_type='multipart/form-data'
    )

    assert response.status_code == 403
    assert response.json["error"] == "You already have an uploaded file. Delete it before uploading a new one."

def test_delete_file(client, mocker):
    # Mock verify_user and delete methods
    mocker.patch('app.routes.upload.verify_user', return_value="test_user_id")
    mocker.patch('app.models.file_metadata.FileMetadata.get_file_metadata', return_value={"storage_type": "dropbox", "location": "test_link"})
    mocker.patch('app.services.file_manager.FileManager.delete_from_dropbox', return_value=True)

    response = client.delete(
        "/file",
        headers={"Authorization": "Bearer test_token"}
    )

    assert response.status_code == 200
    assert response.json["message"] == "File deleted successfully!"

def test_delete_file_not_found(client, mocker):
    # Mock verify_user and return no file metadata
    mocker.patch('app.routes.upload.verify_user', return_value="test_user_id")
    mocker.patch('app.models.file_metadata.FileMetadata.get_file_metadata', return_value=None)

    response = client.delete(
        "/file",
        headers={"Authorization": "Bearer test_token"}
    )

    assert response.status_code == 404
    assert response.json["error"] == "No file found for deletion"
