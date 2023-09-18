import requests
import logging
import traceback
import json


logger = logging.getLogger('kong')


class KongClient:

    def __init__(self, endpoint, token=None, token_header=None):
        self.token_header = token_header
        self.token = token
        self.endpoint = endpoint
        self.request_session = requests.Session()

    def prepare_header(self) -> dict | None:
        header = {
            'Content-Type': 'application/json'
        }

        if self.token and self.token_header:
            header.update({
                self.token_header: self.token
            })

        return header

    @classmethod
    def get_proxies(cls, proxy):

        if not proxy:
            return None

        if proxy.get('user') and proxy.get('password'):
            url = '%s://%s:%s@%s:%s' % (
                proxy['protocol'], proxy['user'], proxy['password'], proxy['host'], proxy['port'])
        else:
            url = '%s://%s:%s' % (
                proxy['protocol'], proxy['host'], proxy['port']
            )

        _p = {
            'https': url,
            'http': url,
        }

        return _p

    def send(self, method, url, params=None, body=None, timeout=30, check_proxy=False, proxies=None):
        method = method.lower()
        if not hasattr(self.request_session, method):
            raise Exception("Do not support method [%s]" % method)

        fn = getattr(self.request_session, method)

        if check_proxy and not proxies:
            return None

        try:
            if proxies:
                rsp = fn(url=url, params=params, json=body, timeout=timeout,
                         headers=self.prepare_header(),
                         proxies=proxies, verify=False)
            else:
                rsp = fn(url=url, params=params, json=body, timeout=timeout,
                         headers=self.prepare_header())

            text = rsp.text
        except Exception as e:
            logger.error(
                'failed to send request to webapi(%s), get exception: %s', url, e)
            logger.error(traceback.format_exc())
            return None

        try:
            return json.loads(text)
        except Exception as e:
            logger.error("failed to load response: %s, exception: %s", text, e)
            return None

    def get_services(self, args=None):
        return self.send('get', self.endpoint + '/services', params=args)

    def add_service(self, args=None):
        return self.send('post', self.endpoint + '/services', body=args)

    def add_route(self, args=None):
        return self.send('post', self.endpoint + '/routes', body=args)

    def add_plugin(self, args=None):
        return self.send('post', self.endpoint + '/plugins', body=args)

    def add_consumer(self, args=None):
        return self.send('post', self.endpoint + '/consumers', body=args)

    def add_key_auth(self, user_id, args=None):
        return self.send('post', self.endpoint + f'/consumers/{user_id}/key-auth', body=args)
