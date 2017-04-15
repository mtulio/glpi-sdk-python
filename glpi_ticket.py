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

from glpi import GlpiService, GlpiInvalidArgument


class Ticket(object):
    """ Object of Item Ticket """

    def __init__(self, name=None, content=None, attributes={}):
        """
        Construct an item Ticket.
        TODO: data could be loaded from an defaults file (JSON, CSV, ...)
        """
        self.null = '<DEFAULT_VALUE>'
        self.data = {
            "name": "<DEFAULT_VALUE>",
            "content": "<DEFAULT_VALUE>",
            "actiontime": 0,
            "begin_waiting_date": self.null,
            "close_delay_stat": 0,
            "closedate": self.null,
            "due_date": self.null,
            "entities_id": 0,
            "global_validation": 1,
            "impact": 3,
            "itilcategories_id": 0,
            "locations_id": 0,
            "priority": 3,
            "requesttypes_id": 1,
            "sla_waiting_duration": 0,
            "slts_tto_id": 0,
            "slts_ttr_id": 0,
            "solution": self.null,
            "solutiontypes_id": 0,
            "solve_delay_stat": 0,
            "solvedate": self.null,
            "status": 1,
            "takeintoaccount_delay_stat": 0,
            "time_to_own": self.null,
            "ttr_slalevels_id": 0,
            "type": 1,
            "urgency": 3,
            "users_id_lastupdater": 2,
            "users_id_recipient": 2,
            "validation_percent": 0,
            "waiting_duration": 0
        }

        if name is None or content is None:
            raise GlpiInvalidArgument(
                'Cannot open a ticket without Name and Content data')
        else:
            self.set_name_and_content(name, content)

        if attributes is not {}:
            self.set_attributes(attributes)

    def get_data(self):
        """ Returns entire Item data.  """
        return self.data

    def get_attr(self, attr):
        """ Returns an specific attribute.  """
        return self.data[attr]

    def set_name_and_content(self, name, content):
        """ Define name and content, required to every new one ticket.  """
        self.data.update({'name': name})
        self.data.update({'content': content})

    def set_attributes(self, attributes={}):
        """ Define attributes to override defaults.  """
        if attributes is {}:
            return

        for k in attributes:
            if k in self.data.keys():
                self.data[k] = attributes[k]
            else:
                self.data.update({k: attributes[k]})

    def get_stream(self):
        """ Get stream of data with format acceptable in GLPI API.  """

        input_data = ""
        null_str = self.null
        for k in self.data:
            if input_data is not "":
                input_data = "%s," % input_data

            if self.data[k] == null_str:
                input_data = '%s "%s": null' % (input_data, k)
            elif isinstance(self.data[k], str):
                input_data = '%s "%s": "%s"' % (input_data, k, self.data[k])
            else:
                input_data = '%s "%s": %s' % (input_data, k, str(self.data[k]))

        return input_data


class GlpiTicket(GlpiService):
    """ Client for GLPI Ticket item """

    def __init__(self, url, app_token, username,
                 password):
        """ Construct an instance for Ticket item """

        uri = '/Ticket'

        GlpiService.__init__(self, url, app_token, uri,
                             username=username, password=password)

    """ CREATE """
    def create(self, name=None, content=None, ticket_data=None):
        if (name is None or content is None) and ticket_data is None:
            return "{ 'error_message' : 'Name or content not found.'}"

        ticket = None
        if ticket_data is not None:
            ticket = ticket_data
        else:
            ticket = Ticket(name, content)

        payload = '{"input": { %s }}' % (ticket.get_stream())
        response = self.request('POST', '/Ticket', data=payload,
                                accept_json=True)

        return response

    """ GET """
    def get(self, item_id):
        """ Return the JSON with Ticket item with ID item_id. """
        if isinstance(item_id, int):
            uri = '/Ticket/%d' % item_id
            response = self.request('GET', uri)
            return response.json()
        else:
            return {'message': 'Unale to get the Ticket ID [%s]' % item_id}

    def get_all(self):
        """ Returns an JSON with the list of tickets. """
        response = self.request('GET', '/Ticket')
        return response.json()

    """ TODO:
    get_by_name()
    search_by_key()
    """
