import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.schemas import KnowledgeBaseMetadata

client = TestClient(app)

# Apply a global mock for get_current_user to prevent real HTTP calls during tests
@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch("app.utils.auth.get_current_user", return_value="test_user_id"):
        yield


@patch("app.routes.knowledge_base.get_storage_provider")
def test_successful_upload(mock_get_storage_provider):
    """
    Test a successful file upload.

    Mocks `get_current_user` to provide a user ID and `get_storage_provider`
    to simulate file upload.

    Asserts:
        - Status code is 200 (OK)
        - Response JSON contains expected metadata fields
    """
    # Mock storage provider to return a test URL upon successful upload
    mock_storage = MagicMock()
    mock_storage.upload_file.return_value = "fakeurl"
    mock_get_storage_provider.return_value = mock_storage

    # Simulate file upload with authorization header
    response = client.post(
        "/api/knowledge-base/upload",
        files={"file": ("test.pdf", b"sample content", "application/pdf")},
        headers={"Authorization": "Bearer test_token"}
    )

    # Validate response status and content
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert response.json() == {
        "user_id": "test_user_id",
        "file_name": "test.pdf",
        "cloud_storage_path": "fakeurl",
        "uploaded_at": response.json()["uploaded_at"]
    }


def test_invalid_file_type():
    """
    Test that uploading an unsupported file type returns a 400 error.

    Tries to upload a file with a .txt extension, which should trigger a validation error.

    Asserts:
        - Status code is 400 (Bad Request)
        - Error message details the invalid file type
    """
    response = client.post(
        "/api/knowledge-base/upload",
        files={"file": ("test.txt", b"sample content", "text/plain")},
        headers={"Authorization": "Bearer test_token"}
    )

    # Verify the error response
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
    assert response.json() == {"detail": "Invalid file type"}


@patch("app.routes.knowledge_base.get_storage_provider")
def test_upload_service_error(mock_get_storage_provider):
    """
    Test server error during file upload.

    Mocks `get_storage_provider` to raise an exception to simulate a server error.

    Asserts:
        - Status code is 500 (Internal Server Error)
        - Error message indicates a server issue
    """
    # Configure the mock to raise an exception
    mock_storage = MagicMock()
    mock_storage.upload_file.side_effect = Exception("Storage provider error")
    mock_get_storage_provider.return_value = mock_storage

    # Simulate file upload with exception
    response = client.post(
        "/api/knowledge-base/upload",
        files={"file": ("test.pdf", b"sample content", "application/pdf")},
        headers={"Authorization": "Bearer test_token"}
    )

    # Verify that the response indicates an internal server error
    assert response.status_code == 500, f"Expected 500 Internal Server Error, got {response.status_code}"
    assert response.json() == {"detail": "An error occurred during file upload"}
