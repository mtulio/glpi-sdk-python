
import json
import time
import sys
import os
from dotenv import load_dotenv, find_dotenv
from glpi import GlpiProfile
from glpi import GlpiTicket, Ticket
from glpi import GlpiKnowBase, KnowBase

load_dotenv(find_dotenv())

def load_from_vcap_services(service_name):
    vcap_services = os.getenv("VCAP_SERVICES")
    print repr(vcap_services)
    if vcap_services is not None:
        services = json.loads(vcap_services)
        if service_name in services:
            return services[service_name][0]["credentials"]
    else:
        return None

def test_profile():
    glpi_pfl = GlpiProfile(url,
                glpi_app_token, username=username,
                password=password)


    print "Getting profile "
    print json.dumps(glpi_pfl.get_my_profiles(),
                     indent=4, separators=(',', ': '))

    token_session = glpi_pfl.get_session_token()
    print "Current session is: %s" % token_session

def test_ticket():
    glpi_ticket = GlpiTicket(url, glpi_app_token,
                             username=username,
                             password=password)

    print "Update Ticket object to session: %s" %\
            glpi_ticket.update_session_token(token_session)

    tickets_all = glpi_ticket.get_all()
    print "Retrieving all tickets: %s" % json.dumps(tickets_all,
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)

    ticket = Ticket(name="New ticket from SDK %s" % t,
                    content=" Content of ticket created by SDK API  %s" % t)
    ticket_dict = glpi_ticket.create(ticket_data=ticket)
    print "Created the ticket: %s" % ticket_dict

    print "Getting ticket recently created with id %d ..." % ticket_dict['id']
    ticket_get = glpi_ticket.get(ticket_dict['id'])
    print "Got this ticket: %s" % json.dumps(ticket_get,
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)

def test_kb():
    kb_item = GlpiKnowBase(url, glpi_app_token,
                             username=username,
                             password=password)

    res = kb_item.get_all()
    print "Retrieving all KBs: %s" % json.dumps(res,
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)

    res = kb_item.get(1)
    print "Retrieve KB ID: %s" % json.dumps(res,
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)

    kb = KnowBase()
    print "Print default KB: %s" % kb.get_attribute('id')
    if res is not None:
        kb.set_attributes(res)
    print "Print default KB: %s" % kb.get_attribute('id')
    print "Retrieving all KBs: %s" % json.dumps(kb.get_stream(),
                          indent=4,
                          separators=(',', ': '),
                          sort_keys=True)

    print "SDK Version: %s" % kb_item.get_version()
    print "SDK Version: %s" % kb_item.__version__

    print "KB Creating new one..."
    name = "New KB Title %s" % t
    subject = "New KB Body %s" % t
    kb2 = KnowBase()
    kb2.set_attribute('name', name)
    kb2.set_attribute('answer', subject)
    res = kb2.get_attributes()
    print "Retrieving KB obj: %s" % json.dumps(res,
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)

    kb_dict = kb_item.create(kb2)
    print "Creating: %s " % kb_dict


if __name__ == '__main__':

    vcap_service_credentials = load_from_vcap_services('glpi')
    url = username = password = glpi_app_token = token_session = ""

    if vcap_service_credentials is not None and isinstance(
                                                vcap_service_credentials, dict):
        url = vcap_service_credentials['url']
        username = vcap_service_credentials['username']
        password = vcap_service_credentials['password']
        glpi_app_token = vcap_service_credentials['app_token']

    else:
        print("Unable to load .env file. Please create using tests/.env.sample")
        sys.exit(1)

    print repr(vcap_service_credentials)
    t = time.strftime("%Y/%m/%d-%H:%M:%S")

    test_profile()
    test_ticket()
    test_kb()
