import base64
import hmac
import os
from hashlib import sha256
from requests.auth import AuthBase
from urllib.parse import urlsplit
from datetime import datetime, timezone

def base64url_encode(input_bytes):
    return base64.urlsafe_b64encode(input_bytes).rstrip(b'=').decode('utf-8')

def base64url_decode(input_str):
    input_str = input_str.replace('-', '+').replace('_', '/')
    padding = '=' * (4 - len(input_str) % 4)
    return base64.b64decode(input_str + padding)

class VerintHmac(AuthBase):
    SIGNATURE_PREFIX = 'Vrnt-1-HMAC-SHA256'

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        self._encode(request)
        return request

    def _encode(self, request):
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        self._add_signature(request, timestamp)
        request.headers['Content-Type'] = 'application/json'

    def _add_signature(self, request, timestamp):
        method = request.method
        url_components = urlsplit(request.url)
        path = url_components.path

        random_bytes = os.urandom(16)
        salt = base64url_encode(random_bytes)

        string_to_sign = f'{salt}\n{method}\n{path}\n{timestamp}\n\n'
        signature = self._sign(string_to_sign)
        auth_header_value = (f'{VerintHmac.SIGNATURE_PREFIX} salt={salt},'
                             f'iat={timestamp},kid={self.api_key},sig={signature}')
        request.headers['Authorization'] = auth_header_value

    def _sign(self, string_to_sign):
        decoded_secret_key = base64url_decode(self.secret_key)
        hash = hmac.new(decoded_secret_key, string_to_sign.encode('utf-8'), sha256)
        return base64url_encode(hash.digest())