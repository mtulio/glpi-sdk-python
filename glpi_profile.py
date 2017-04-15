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

from glpi import GlpiService


class GlpiProfile(GlpiService):
    """ Client for GLPI Profile item """

    def __init__(self, url, app_token, username=None,
                 password=None):
        """ Construct an instance for Profile item. """

        myuri = '/getMyProfiles/'

        GlpiService.__init__(
            self, url, app_token, myuri, username=username,
            password=password)

    def get_my_profiles(self):
        """
        Returns profile entitie for user authenticated here.
        This is an example and no secure to be exposed. :)
        """
        response = self.request('GET', self.uri)
        return response.json()
