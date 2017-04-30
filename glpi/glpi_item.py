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


class GlpiItem(object):
    """ Polymorphic class of GLPI Item object. """

    def __init__(self, data={}):
        self.data = data
        self.null_str = "<DEFAULT_NULL>"

    def get_data(self):
        """ Returns entire attributes of Item data. """
        return self.data

    def get_attributes(self):
        """ Return an specific attribute of Item data. """
        return self.get_data()

    def get_attribute(self, attr):
        """ Returns an specific attribute. """
        if attr in self.data:
            return self.data[attr]

    def set_attribute(self, attr, value):
        """ Define the 'value' to an key. """
        self.data[attr] = value

    def set_attributes(self, attributes={}):
        """ Define attributes to override defaults.  """
        if attributes is {}:
            return self.data

        for k in attributes:
            if k in self.data.keys():
                self.data[k] = attributes[k]
            else:
                self.data.update({k: attributes[k]})

    def unset_attributes(self):
        """ Clean all attributes. """
        self.data = {}
        return self.data

    def get_stream(self):
        """ Get stream of data with format acceptable in GLPI API.  """
        input_data = ""
        for k in self.data:
            if input_data is not "":
                input_data = "%s," % input_data

            if self.data[k] == self.null_str:
                input_data = '%s "%s": null' % (input_data, k)
            elif isinstance(self.data[k], str):
                input_data = '%s "%s": "%s"' % (input_data, k, self.data[k])
            else:
                input_data = '%s "%s": %s' % (input_data, k, str(self.data[k]))

        return input_data
