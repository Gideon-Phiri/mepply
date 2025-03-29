import requests
from config import AUTH_SERVICE_URL
import logging


def verify_user(auth_header: str | None):  # Type hint for clarity
    """Verify user token."""

    if not auth_header:
        logging.warning("Authorization header is missing.")
        return None, None

    try:
        parts = auth_header.split()  # Split the header value
        if len(parts) != 2 or parts[0].lower() != "bearer":  # Robust check
            logging.warning("Authorization header is malformed (not 'Bearer <token>').")
            return None, None
        auth_token = parts[1]
    except IndexError:  # Handle potential IndexError after split
        logging.warning("Authorization header is malformed (no token provided).")
        return None, None
    except AttributeError:
        logging.warning("Authorization header is not a string.")
        return None, None

    headers = {"Authorization": f"Bearer {auth_token}"}
    logging.debug(f"Sending request to auth-service with headers: {headers}")
    logging.debug(f"Auth Service URL: {AUTH_SERVICE_URL}")

    try:
        response = requests.get(AUTH_SERVICE_URL, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        user_data = response.json()
        return user_data.get("userId"), user_data
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error communicating with auth-service: {http_err}")
        if response.status_code == 401:
            logging.warning("Authorization token is missing or invalid.")
        elif response.status_code == 403:
            logging.warning("User is unauthorized.")
        return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with auth-service: {e}")
        return None, None
