import requests
from config import AUTH_SERVICE_URL
import logging

def verify_user(auth_token):
    """Send a request to the auth-service to verify the user token."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    logging.debug(f"Sending request to auth service with headers: {headers}")
    logging.debug(f"Auth Service URL: {AUTH_SERVICE_URL}")

    try:
        response = requests.get(AUTH_SERVICE_URL, headers=headers)
        logging.debug(f"Auth service response status: {response.status_code}")
        logging.debug(f"Auth service response data: {response.json()}")
        
        if response.status_code == 200:
            return response.json().get("userId")
    except requests.exceptions.RequestException as e:
        logging.error(f"Auth service error: {e}")
    return None
