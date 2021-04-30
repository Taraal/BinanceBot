import requests
import json
import hmac
import time
import hashlib
import asyncio
import websockets

from requests.exceptions import ConnectionError
from http.client import RemoteDisconnected, HTTPException

class BinanceAPI(object):

    URL = "https://api.binance.com/"
    STREAM_URL = "wss://stream/binance:9443"

    ##### INIT #####

    def __init__(self, api_key=None, api_secret=None):

        self.key = api_key
        self.secret = api_secret
        self.session = requests.session()
        self.session.headers.update({"Accept": 'application/x-www-form-urlencoded',
                                    "X-MBX-APIKEY": self.key})

    def _request(self, endpoint, params, http_method):
        headers = {"Accept": 'application/json',
                                    "X-MBX-APIKEY": self.key}
        #resp = getattr(self.session, http_method)(BinanceAPI.URL + endpoint, params=params)

        resp = requests.get(BinanceAPI.URL + endpoint, headers=headers, params=params)
        print(BinanceAPI.URL + endpoint)
        if resp.status_code == 200:
            return json.loads(resp.text)
        return resp.text
    
    ##### HTTP METHODS #####

    def _get(self, endpoint, params=None):
        return self._request(endpoint, params, "get")

    def _post(self, endpoint, params=None):
        print(endpoint)
        return self._request(endpoint, params, "post")

    def _put(self, endpoint, params=None):
        return self._request(endpoint, params, "put")

    # No need for delete method #

    ##### SECURITY #####

    def _get_signature(self, data):
        assert(self.key and self.secret)

        url_data = "&".join(['%s=%s' % (k,v) for k,v in data.items()])

        return hmac.new(bytes(self.secret, 'utf-8'), msg=url_data.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

    def _get_timestamp(self):

        return int(time.time() * 1000)

    
    def _add_security_params(self, data):

        data['timestamp'] = self._get_timestamp()
        data['signature'] = self._get_signature(data)

        return data

    ##### API METHODS #####

    def get_account_status(self):
        assert(self.key)

        params = {}

        
        params = self._add_security_params(params)

        res = self._get('api/v3/account', params)

        return res

    def get_history(self):

        assert(self.key)

        par

    def status(self):
        return self._get('sapi/v1/system/status')


    def new_stream(self):
        assert(self.key)

        res = self._post('api/v3/userDataStream/')
        print(res)
        return res['listenKey']

    def keepalive_stream(self, listenKey):
        assert(self.key)

        param = "listenKey=%s" % (listenKey)

        return self._put('api/v3/userDataStream', param)

    async def listen(self):
        uri = "wss://stream.binance.com:9443/stream?stream=" + self.new_stream()

        print(uri)
        async with websockets.connect(uri) as websocket:
            test = await websocket.recv()

            print("Test : ", test)