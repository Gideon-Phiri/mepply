# tests/test_upload.py
import pytest
from unittest.mock import patch, MagicMock
from app.routes.upload import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_upload_file(client, mocker):
    mocker.patch('app.routes.upload.verify_user', return_value="test_user_id")
    mocker.patch('app.models.file_metadata.FileMetadata.get_file_metadata', return_value=None)
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
