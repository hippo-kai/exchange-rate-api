import json
import re
import requests


class APIRequest:
    config = {}
    headers = {}
    account_id = ''

    def __init__(self, config, token, account_id):
        self.config = config
        self.headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        self.default_params = {
            'account_id': account_id
        }


    def execute(self, command='', params={}, queries={}, payload={}):
        if command == '':
            raise Exception('Please set command of API request!')

        try:
            request_params = self.__format_request_params(command, params, queries)
            print(request_params)
            response = requests.request(*request_params, headers=self.headers, data=payload)
            return response.json()

        except Exception as error:
            raise error


    def __format_request_params(self, command, params, queries):
        api_config = self.config['endpoints']
        for key in command.split('.'):
            if key not in api_config:
                raise Exception('No config for the target command "{}".'.format(command))
            api_config = api_config[key]

        url = self.__format_url(api_config, params, queries)

        return [api_config['method'], url]


    def __format_url(self, api_config, params, queries):
        url = '{url}/{path}'.format(url=self.config['url'], path=api_config['path'])

        url_params = self.default_params | params
        for (key, value) in self.default_params.items():
            url = url.replace('<{}>'.format(key), value)

        for i, (key, value) in enumerate(queries.items()):
            url = '{0}{1}{2}={3}'.format(url, '?' if i == 0 else '&', key, value)

        return url
