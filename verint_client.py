import requests
from hmac_auth import VerintHmac
import logging
from config import BASE_URL, API_KEY_ID, API_KEY_SECRET

class VerintClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.api_key_id = API_KEY_ID
        self.api_key_val = API_KEY_SECRET

    def verint_call(self, endpoint, method="GET", request_body=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logging.info(f"Calling Verint API [{method}] => {url}")

        headers = {'Content-Type': 'application/json'}
        auth = VerintHmac(self.api_key_id, self.api_key_val)

        response = requests.request(method, url, headers=headers, auth=auth, json=request_body)
        response.raise_for_status()
        return response.json()