"""
Module: verint_client.py
Purpose: Defines a client for making authenticated requests to the Verint API
using HMAC authentication.
"""

import requests
from hmac_auth import VerintHmac
import logging
from config import BASE_URL, API_KEY_ID, API_KEY_SECRET

class VerintClient:
    """
    A client to interact with the Verint API using HMAC authentication.
    """

    def __init__(self):
        """
        Initializes the VerintClient with API credentials and base URL.
        """
        self.base_url = BASE_URL
        self.api_key_id = API_KEY_ID
        self.api_key_val = API_KEY_SECRET

    def verint_call(self, endpoint, method="GET", request_body=None):
        """
        Makes an authenticated request to the Verint API.

        Args:
            endpoint (str): API endpoint to be called (relative to base_url).
            method (str): HTTP method (default is 'GET').
            request_body (dict, optional): JSON body to be sent with the request.

        Returns:
            dict: Parsed JSON response from the API.

        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        # Construct the full URL by appending the endpoint to the base URL
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logging.info(f"Calling Verint API [{method}] => {url}")

        # Set required headers for the request
        headers = {'Content-Type': 'application/json'}

        # Generate HMAC authentication header
        auth = VerintHmac(self.api_key_id, self.api_key_val)

        # Make the HTTP request
        response = requests.request(method, url, headers=headers, auth=auth, json=request_body)

        # Raise an exception for unsuccessful responses
        response.raise_for_status()

        # Return the parsed JSON response
        return response.json()