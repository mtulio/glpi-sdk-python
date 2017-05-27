# Copyright 2017 Predict & Truly Systems All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# GLPI API Rest documentation:
# https://github.com/glpi-project/glpi/blob/9.1/bugfixes/apirest.md

import json as json_import
import requests
from requests.structures import CaseInsensitiveDict
import os

from version import __version__


def load_from_vcap_services(service_name):
    vcap_services = os.getenv("VCAP_SERVICES")
    if vcap_services is not None:
        services = json_import.loads(vcap_services)
        if service_name in services:
            return services[service_name][0]["credentials"]
    else:
        return None


def _remove_null_values(dictionary):
    if isinstance(dictionary, dict):
        return dict([(k, v) for k, v in dictionary.items() if v is not None])
    return dictionary


def _cleanup_param_value(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    return value


def _cleanup_param_values(dictionary):
    if isinstance(dictionary, dict):
        return dict(
            [(k, _cleanup_param_value(v)) for k, v in dictionary.items()])
    return dictionary


class GlpiException(Exception):
    pass


class GlpiInvalidArgument(GlpiException):
    pass


class GlpiService(object):
    """ Polymorphic class of GLPI REST API Service. """
    __version__ = __version__

    def __init__(self, url_apirest, token_app, uri,
                 username=None, password=None, token_auth=None,
                 use_vcap_services=False, vcap_services_name=None):
        """
        [TODO] Loads credentials from the VCAP_SERVICES environment variable if
        available, preferring credentials explicitly set in the request.
        If VCAP_SERVICES is not found (or use_vcap_services is set to False),
        username and password credentials must be specified.

        You can choose in setup initial authentication using username and
        password, or setup with Authorization HTTP token. If token_auth is set,
        username and password credentials must be ignored.
        """
        self.__version__ = __version__
        self.url = url_apirest
        self.app_token = token_app
        self.uri = uri

        self.username = username
        self.password = password
        self.token_auth = token_auth

        self.session = None

        if token_auth is not None:
            if username is not None or password is not None:
                raise GlpiInvalidArgument(
                    'Cannot set token_auth and username and password together')
            self.set_token_auth(token_auth)
        else:
            self.set_username_and_password(username, password)

        if use_vcap_services and not self.username and not self.token_auth:
            self.vcap_service_credentials = load_from_vcap_services(
                vcap_services_name)
            if self.vcap_service_credentials is not None and isinstance(
                    self.vcap_service_credentials, dict):
                self.url = self.vcap_service_credentials['url']
                if 'username' in self.vcap_service_credentials:
                    self.username = self.vcap_service_credentials['username']
                if 'password' in self.vcap_service_credentials:
                    self.password = self.vcap_service_credentials['password']
                if 'token_auth' in self.vcap_service_credentials:
                    self.token_auth =\
                        self.vcap_service_credentials['token_auth']
                if 'app_token' in self.vcap_service_credentials:
                    self.app_token = self.vcap_service_credentials['app_token']

        if self.app_token is None:
            raise GlpiException(
                'You must specify GLPI API-Token(app_token) to make API calls')

        if (self.username is None or self.password is None)\
                and self.token_auth is None:
            raise GlpiException(
                'You must specify your username and password, or token_auth'
                'service credentials ')

    def set_username_and_password(self, username=None, password=None):
        if username == 'YOUR SERVICE USERNAME':
            username = None
        if password == 'YOUR SERVICE PASSWORD':
            password = None

        self.username = username
        self.password = password

    def set_token_auth(self, token_auth):
        if token_auth == 'YOUR AUTH TOKEN':
            token_auth = None

        self.token_auth = token_auth

    def set_uri(self, uri):
        self.uri = uri

    def get_version(self):
        return self.__version__

    """
    Session Token
    """
    def set_session_token(self):
        """ Set up new session ID """

        # URL should be like: http://glpi.example.com/apirest.php
        full_url = self.url + '/initSession'
        auth = None

        headers = {"App-Token": self.app_token,
                   "Content-Type": "application/json"}

        if self.token_auth is not None:
            auth = self.token_auth
        else:
            auth = (self.username, self.password)

        r = requests.request('GET', full_url,
                             auth=auth, headers=headers)

        try:
            self.session = r.json()['session_token']
            return True
        except Exception as e:
            raise Exception("Unable to init session in GLPI server: %s" % e)

        return False

    def get_session_token(self):
        """ Returns current session ID """

        if self.session is not None:
            return self.session
        else:
            if self.set_session_token():
                return self.session
            else:
                return 'Unable to get Session Token'

    def update_session_token(self, session_id):
        """ Update session ID """

        if session_id:
            self.session = session_id

        return self.session

    """ Request """
    def request(self, method, url, accept_json=False, headers={},
                params=None, json=None, data=None, files=None, **kwargs):
        """
        Make a request to GLPI Rest API.
        Return response object.
        (http://docs.python-requests.org/en/master/api/#requests.Response)
        """

        full_url = self.url + url
        if self.session is None:
            new_session = True

        input_headers = _remove_null_values(headers) if headers else {}

        headers = CaseInsensitiveDict(
             {'user-agent': 'glpi-sdk-python-' + __version__})

        if accept_json:
            headers['accept'] = 'application/json'

        try:
            if self.session is None:
                self.set_session_token()
            headers.update({'Session-Token': self.session})
        except Exception as e:
            raise Exception("Unable to get Session token. ERROR: %s" % e)

        if self.app_token is not None:
            headers.update({'App-Token': self.app_token})

        headers.update(input_headers)

        # Remove keys with None values
        params = _remove_null_values(params)
        params = _cleanup_param_values(params)
        json = _remove_null_values(json)
        data = _remove_null_values(data)
        files = _remove_null_values(files)

        try:
            response = requests.request(method=method, url=full_url,
                                        headers=headers, params=params,
                                        data=data, **kwargs)
        except Exception:
            raise

        return response

    def get_payload(self, data_json):
        """ Construct the payload for REST API from JSON data. """

        data_str = ""
        null_str = "<DEFAULT_NULL>"
        for k in data_json:
            if data_str is not "":
                data_str = "%s," % data_str

            if data_json[k] == null_str:
                data_str = '%s "%s": null' % (data_str, k)
            elif isinstance(data_json[k], str):
                data_str = '%s "%s": "%s"' % (data_str, k, data_json[k])
            else:
                data_str = '%s "%s": %s' % (data_str, k, str(data_json[k]))

        return data_str

    """ Generic Items methods """
    # [C]REATE - Create an Item
    def create(self, data_json=None):
        """ Create an object Item. """

        if (data_json is None):
            return "{ 'error_message' : 'Object not found.'}"

        payload = '{"input": { %s }}' % (self.get_payload(data_json))

        try:
            response = self.request('POST', self.uri, data=payload,
                                    accept_json=True)
        except Exception as e:
            print "#>> ERROR requesting uri(%s) payload(%s)" % (uri, payload)
            raise

        return response.json()

    # [R]EAD - Retrieve Item data
    def get_all(self):
        """ Return all content of Item in JSON format. """

        res = self.request('GET', self.uri)
        return res.json()

    def get(self, item_id):
        """ Return the JSON item with ID item_id. """

        if isinstance(item_id, int):
            uri = '/%s/%d' % (self.uri, item_id)
            response = self.request('GET', uri)
            return response.json()
        else:
            return {'error_message': 'Unale to get %s ID [%s]' % (self.uri,
                                                                  item_id)}

    def get_path(self, path=''):
        """ Return the JSON from path """
        uri = '/%s' % (path)
        response = self.request('GET', uri)
        return response.json()

    def search_options(self, item_name):
        """
        List search options for an Item to be used in
        search_engine/search_query.
        """
        new_uri = "%s/%s" % (self.uri, item_name)
        response = self.request('GET', new_uri, accept_json=True)

        return response.json()

    def search_engine(self, search_query):
        """
        Search an item by URI.
        Use GLPI search engine passing parameter by URI.
        #TODO could pass search criteria in payload, like others items
        operations.
        """
        new_uri = "%s/%s" % (self.uri, search_query)
        response = self.request('GET', new_uri, accept_json=True)

        return response.json()

    # [U]PDATE an Item
    def update(self, data):
        """ Update an object Item. """

        payload = '{"input": { %s }}' % (self.get_payload(data))
        new_url = "%s/%d" % (self.uri, data['id'])

        try:
            response = self.request('PUT', self.uri, data=payload)
        except Exception as e:
            print {
                "message_error": "ERROR requesting uri(%s) payload(%s)" % (
                                    uri, payload)
            }
            raise

        return response.json()

    # [D]ELETE an Item
    def delete(self, item_id, force_purge=False):
        """ Delete an object Item. """

        if not isinstance(item_id, int):
            return {"message_error": "Please define item_id to be deleted."}

        if force_purge:
            payload = '{"input": { "id": %d } "force_purge": true}' % (item_id)
        else:
            payload = '{"input": { "id": %d }}' % (item_id)

        try:
            response = self.request('DELETE', self.uri, data=payload)
        except Exception as e:
            print {
                "message_error": "ERROR requesting uri(%s) payload(%s)" % (
                                    uri, payload)
            }
            raise
        return response.json()


class GLPI(object):
    """
    Generic implementation of GLPI Items can manage all
    Itens in one GLPI server connection.
    We can use this class to save implementation of "new classes" and
    can reuse API sessions.
    To support new items you should create the dict key/value in item_map.
    """
    __version__ = __version__

    def __init__(self, url, app_token, auth_token,
                 item_map=None):
        """ Construct generic object """

        self.url = url
        self.app_token = app_token
        self.auth_token = auth_token

        self.item_uri = None
        self.item_map = {
            "ticket": "/Ticket",
            "knowbase": "/knowbaseitem",
            "listSearchOptions": "/listSearchOptions",
            "search": "/search",
            "user": "user",
            "getFullSession": "getFullSession",
            "getActiveProfile": "getActiveProfile",
            "getMyProfiles": "getMyProfiles",
        }
        self.api_rest = None
        self.api_session = None

        if item_map is not None:
            self.set_item_map(item_map)

    def help_item(self):
        """ Help item values """
        return {"available_items": self.item_map}

    def set_item(self, item_name):
        """ Define an item to object """
        self.item_uri = self.item_map[item_name]

    def set_item_map(self, item_map={}):
        """ Set an custom item_map. """
        self.item_map = item_map

    def set_api_uri(self):
        """
        Update URI in Service API object.
        We should do this every new Item requested.
        """
        self.api_rest.set_uri(self.item_uri)

    def init_api(self):
        """ Initialize the API Rest connection """
        if self.item_uri is None:
            return {"message_error": "Please use set_item() before init API."}

        self.api_rest = GlpiService(self.url, self.app_token,
                                    self.item_uri, token_auth=self.auth_token)

        self.api_session = self.api_rest.get_session_token()

        if self.api_session is not None:
            return {"session_token": self.api_session}
        else:
            return {"message_error": "Unable to InitSession in GLPI Server."}

    def init_item(self, item_name):
        """ Initialize an Item context. """
        update_api = False

        if self.item_uri != self.item_map[item_name]:
            self.set_item(item_name)
            update_api = True

        if self.api_rest is None:
            try:
                self.init_api()
            except:
                print "message_error: Unable to InitSession in GLPI Server."
                return False

        if update_api:
            self.set_api_uri()

        return True

    # [C]REATE - Create an Item
    def create(self, item_name, item_data):
        """ Create an Resource Item """
        if not self.init_item(item_name):
            return {"message_error": "Unable to create an Item in GLPI Server"}

        return self.api_rest.create(item_data)

    # [R]EAD - Retrieve Item data
    def get_all(self, item_name):
        """ Get all resources from item_name """
        if not self.init_item(item_name):
            return {"message_error": "Unable to get Item in GLPI Server."}

        return self.api_rest.get_all()

    def get(self, item_name, item_id=None):
        """ Get item_name and/with resource by ID """

        if item_id is None:
            return self.api_rest.get_path(item_name)

        if not self.init_item(item_name):
            return {"message_error": "Unable to get Item by ID in GLPI Server"}

        return self.api_rest.get(item_id)

    def search_options(self, item_name):
        """ List GLPI APIRest Search Options """
        if not self.init_item('listSearchOptions'):
            return {"message_error": "Unable to create an Item in GLPI Server"}

        return self.api_rest.search_options(item_name)

    def search_criteria(self, data, criteria):
        """ #TODO Search in data some criteria """
        result = []
        for d in data:
            find = False
            for c in criteria:
                if c['value'].lower() in d[c['field']].lower():
                    find = True
            if find:
                result.append(d)
        return result

    def search_metacriteria(self, metacriteria):
        """ TODO: Search in metacriteria in source Item """
        return {"message_info": "Not implemented yet"}

    def search(self, item_name, criteria):
        """ #SHOULD BE IMPROVED
        Return an Item with that matchs with criteria
        criteria: [
            {
                "field": "name",
                "value": "search value"
            }
        ]
        """
        if 'criteria' in criteria:
            data = self.get_all(item_name)
            return self.search_criteria(data, criteria['criteria'])
        elif 'metacriteria' in criteria:
            return self.search_metacriteria(criteria['metacriteria'])
        else:
            return {"message_error": "Unable to find a valid criteria."}

    def search_engine(self, item_name, criteria):
        """ Call GLPI's search engine syntax.
        Ex. cURL - usage to query in 'name' and return ID:
        $ curl -X GET  ... 'http://path/to/apirest.php/search/Knowbaseitem?\
            criteria\[0\]\[field\]\=6\
            &criteria\[0\]\[searchtype\]=contains\
            &criteria\[0\]\[value\]=sites-multimidia\
            &criteria\[0\]\[link\]\=AND\
            &criteria\[1\]\[field\]\=2\
            &criteria\[1\]\[searchtype\]\=contains\
            &criteria\[1\]\[value\]\=\
            &criteria\[1\]\[link\]\=AND' |jq .

        INPUT query in JSON format (/apirest.php#search-items):
        metacriteria: [
            {
                "link": 'AND'
                "searchtype": "contais",
                "field": "name",
                "value": "search value"
            }
        ]

        RETURNS:
        GLPIs APIREST JSON formated with result of search in key 'data'.
        """
        field_map = {
            "id": 2,
            "name": 6,
            "body": 6,
        }
        s_index = 0
        uri_query = "%s?" % item_name

        for c in criteria['criteria']:
            if s_index == 0:
                uri = ""
            else:
                uri = "&"

            uri = uri + "criteria[%d][field]=%d&" % (s_index,
                                                     field_map[c['field']])
            if c['value'] is None:
                uri = uri + "criteria[%d][value]=&" % (s_index)
            else:
                uri = uri + "criteria[%d][value]=%s&" % (s_index, c['value'])
            uri = uri + "criteria[%d][searchtype]=%s&" % (s_index,
                                                          c['searchtype'])
            uri = uri + "criteria[%d][link]=%s" % (s_index, c['link'])
            uri_query = uri_query + uri
            s_index += 1

        if not self.init_item('search'):
            return {"message_error": "Unable to search Item in GLPI Server"}

        return self.api_rest.search_options(uri_query)

    # [U]PDATE an Item
    def update(self, item_name, data):
        """ Update an Resource Item. Should have all the Item payload """
        if not self.init_item(item_name):
            return {"message_error": "Unable to init Item in GLPI Server."}

        return self.api_rest.update(data)

    # [D]ELETE an Item
    def delete(self, item_name, item_id, force_purge=False):
        """ Delete an Resource Item. Should have all the Item payload """
        if not self.init_item(item_name):
            return {"message_error": "Unable to init Item in GLPI Server."}

        return self.api_rest.delete(item_id, force_purge=force_purge)
