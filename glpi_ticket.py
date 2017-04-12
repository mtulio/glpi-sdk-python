from .glpi import GlpiService


class GlpiTicket(GlpiService):
    """ Client for GLPI Ticket item """

    def __init__(self, url, app_token, username,
                 password):
        """ Construct an instance for Ticket item """

        GlpiService.__init__(
            self, url, app_token, username=username,
            password=password)

        #self.version = version

    def get_tickets(self):
        """ Returns lsit of tickets. """
        response = self.request('GET', '/listSearchOptions/Ticket')
        return json.dumps(response.json(),
                          indent=4,
                          separators=(',', ': '),
                          sort_keys=True)
