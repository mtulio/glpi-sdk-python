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

from .glpi import GlpiService, GlpiInvalidArgument
from .glpi_item import GlpiItem


class Ticket(GlpiItem):
    """ Object of Item Ticket """

    def __init__(self, name=None, content=None, attributes={}):
        """
        Construct an item Ticket.
        TODO: data could be loaded from an defaults file (JSON, CSV, ...)
        """
        GlpiItem.__init__(self, {})

        defaults = {
            "name": "<DEFAULT_VALUE>",
            "content": "<DEFAULT_VALUE>",
            "actiontime": 0,
            "begin_waiting_date": self.null_str,
            "close_delay_stat": 0,
            "closedate": self.null_str,
            "due_date": self.null_str,
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
            "solution": self.null_str,
            "solutiontypes_id": 0,
            "solve_delay_stat": 0,
            "solvedate": self.null_str,
            "status": 1,
            "takeintoaccount_delay_stat": 0,
            "time_to_own": self.null_str,
            "ttr_slalevels_id": 0,
            "type": 1,
            "urgency": 3,
            "users_id_lastupdater": 2,
            "users_id_recipient": 2,
            "validation_percent": 0,
            "waiting_duration": 0
        }
        self.set_attributes(attributes=defaults)

        if name is None or content is None:
            raise GlpiInvalidArgument(
                'Cannot open a ticket without Name and Content data')
        else:
            """ Define name and content, required to every new one ticket.  """
            self.set_attribute('name', name)
            self.set_attribute('content', content)

        if attributes is not {}:
            self.set_attributes(attributes)


class GlpiTicket(GlpiService):
    """ Client for GLPI Ticket item """

    def __init__(self, url, app_token, username,
                 password):
        """ Construct an instance for Ticket item """

        uri = '/Ticket'

        GlpiService.__init__(self, url, app_token, uri,
                             username=username, password=password)

    """ CREATE """
    def new(self, name=None, content=None, ticket_data=None):
        """
        This is wrapper of polymorphic create() method.
        new() will called when an object Ticket is not create with name set up.
        In general we advise to use create().
        """

        if (name is None or content is None) and ticket_data is None:
            return "{ 'error_message' : 'Name or content not found.'}"

        ticket = None
        if ticket_data is None:
            ticket = Ticket(name, content)
        else:
            ticket = ticket_data

        return self.create(ticket)

    """ TODO:
    get_by_name()
    search_by_key()
    """
