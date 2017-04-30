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


class KnowBase(GlpiItem):
    """ Object of KB """

    def __init__(self, attributes={}):
        """ Construct an KB Item. """
        GlpiItem.__init__(self, {})

        defaults = {
            "knowbaseitemcategories_id": 0,
            "users_id": 2,
            "is_faq": 0,
            "view": 1
        }
        self.set_attributes(attributes=attributes)
        self.set_attributes(attributes=defaults)


class GlpiKnowBase(GlpiService):
    """ Client for GLPI Knowledge Base item """

    def __init__(self, url, app_token, username,
                 password):
        """ Construct an instance for Ticket item """

        uri = '/Knowbaseitem'

        GlpiService.__init__(self, url, app_token, uri,
                             username=username, password=password)
