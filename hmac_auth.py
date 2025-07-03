"""
Module: hmac_auth.py
Purpose: Implements Verint HMAC-based authentication for secure API requests.
This class is used to generate HMAC-signed Authorization headers for Verint API.
"""

import base64
import hmac
import os
from hashlib import sha256
from requests.auth import AuthBase
from urllib.parse import urlsplit
from datetime import datetime, timezone

def base64url_encode(input_bytes):
    """
    Encodes bytes to a base64 URL-safe string without padding.

    Args:
        input_bytes (bytes): Data to encode.

    Returns:
        str: URL-safe base64-encoded string.
    """
    return base64.urlsafe_b64encode(input_bytes).rstrip(b'=').decode('utf-8')

def base64url_decode(input_str):
    """
    Decodes a base64 URL-safe string back to bytes.

    Args:
        input_str (str): Base64-encoded string.

    Returns:
        bytes: Decoded byte data.
    """
    
    input_str = input_str.replace('-', '+').replace('_', '/')
    padding = '=' * (-len(input_str) % 4)  # Ensure proper padding
    return base64.b64decode(input_str + padding)

class VerintHmac(AuthBase):
    """
    Custom HMAC authentication class for Verint API.
    Automatically adds Authorization headers using Verint's signing protocol.
    """

    SIGNATURE_PREFIX = 'Vrnt-1-HMAC-SHA256'

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        """
        Overrides AuthBase callable. Adds signature to the request.

        Args:
            request (requests.PreparedRequest): The outgoing request.

        Returns:
            requests.PreparedRequest: Signed request.
        """
        self._encode(request)
        return request

    def _encode(self, request):
        """
        Encodes the request with current timestamp and signature.
        """
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        self._add_signature(request, timestamp)
        request.headers['Content-Type'] = 'application/json'

    def _add_signature(self, request, timestamp):
        """
        Generates and adds the HMAC Authorization header to the request.

        Args:
            request (requests.PreparedRequest): The request object.
            timestamp (str): The current UTC timestamp.
        """
        method = request.method
        url_components = urlsplit(request.url)
        path = url_components.path

        # Generate a cryptographically secure random salt
        random_bytes = os.urandom(16)
        salt = base64url_encode(random_bytes)

        # Construct the string to sign
        string_to_sign = f'{salt}\n{method}\n{path}\n{timestamp}\n\n'

        # Compute the signature
        signature = self._sign(string_to_sign)

        # Construct Authorization header value
        auth_header_value = (f'{VerintHmac.SIGNATURE_PREFIX} salt={salt},'
                             f'iat={timestamp},kid={self.api_key},sig={signature}')
        request.headers['Authorization'] = auth_header_value

    def _sign(self, string_to_sign):
        """
        Computes the HMAC-SHA256 signature.

        Args:
            string_to_sign (str): The string to sign.

        Returns:
            str: base64 URL-encoded HMAC signature.
        """
        # Decode the base64 URL-safe secret key
        decoded_secret_key = base64url_decode(self.secret_key)

        # Sign the string using HMAC-SHA256
        hash = hmac.new(decoded_secret_key, string_to_sign.encode('utf-8'), sha256)

        # Return the URL-safe base64 encoded signature
        return base64url_encode(hash.digest())