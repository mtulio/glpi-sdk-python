
import json
import time
import sys
import os
from dotenv import load_dotenv, find_dotenv
from glpi import GlpiProfile
from glpi import GlpiTicket, Ticket
from glpi import GlpiKnowBase, KnowBase
from glpi import GLPI

load_dotenv(find_dotenv())

def load_from_vcap_services(service_name):
    vcap_services = os.getenv("VCAP_SERVICES")
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

    print "##> Update Ticket object to session: %s" %\
            glpi_ticket.update_session_token(token_session)

    tickets_all = glpi_ticket.get_all()
    print "Retrieving all tickets: %s" % json.dumps(tickets_all,
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)

    ticket = Ticket(name="New ticket from SDK %s" % t,
                    content=" Content of ticket created by SDK API  %s" % t)
    ticket_dict = glpi_ticket.create(ticket.get_data())
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

    kb_dict = kb_item.create(kb2.get_data())
    print "Creating: %s " % kb_dict


def test_general():

    # Basic usage
    glpi = GLPI(url, glpi_app_token, (username, password))

    print "#> Getting help()"
    print glpi.help_item()

    print "#> Getting standard items: ticket"
    print json.dumps(glpi.get_all('ticket'),
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)

    print "#> Setting up new items..."
    new_map = {
        "ticket": "/Ticket",
        "knowbase": "/knowbaseitem",
        "problem": "/problem",
        "change": "/change",
        "computer": "/computer",
        "software": "/software",
        "network": "/networkequipment",
    }
    glpi.set_item_map(new_map)
    print "#> Getting new item: COMPUTER"
    print json.dumps(glpi.get_all('computer'),
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)

    # Setting up new map
    print "#####> Creating new MAP..."
    new_map = {
         "knowbase": "/knowbaseitem"
    }
    glpi2 = GLPI(url, glpi_app_token, (username, password),
                 item_map=new_map)

    print "#> Getting item: KB"
    print json.dumps(glpi2.get_all('knowbase'),
                       indent=4,
                       separators=(',', ': '),
                       sort_keys=True)

    print "#> Getting item KB by ID 1"
    kb_dict = glpi2.get('knowbase', 1)
    print json.dumps(kb_dict,
                       indent=4,
                       separators=(',', ': '),
                       sort_keys=True)
    print kb_dict
    print "#> Creating new KB copying from previous..."
    kb_data = {
        "name": "New KB copyied from ID %s at %s" % (
                                        kb_dict['id'], t),
        "answer": "Description of KB: \n <br> API Desc </br> Just a test ",
        "is_faq": kb_dict['is_faq'],
        "knowbaseitemcategories_id": kb_dict['knowbaseitemcategories_id'],
        "users_id": kb_dict['users_id'],
        "view": kb_dict['view']
    }
    print "Creating object data: %s" % repr(kb_data)
    kb_res = glpi2.create('knowbase', kb_data)
    print json.dumps(kb_res,
                     indent=4,
                     separators=(',', ': '),
                     sort_keys=True)


def test_general_search():
    glpi = GLPI(url, glpi_app_token, (username, password))

    print "#> Getting help()"
    print glpi.help_item()

    print glpi.init_item('listSearchOptions')

    token_session = glpi.api_session
    print ">>>> Current session is: %s" % token_session

    print "#> Getting search options"
    print json.dumps(glpi.search_options('knowbaseitem'),
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)


def test_search():

    glpi = GLPI(url, glpi_app_token, (username, password))

    criteria = {"criteria": [{"field": "name", "value":"portal"}]}
    print "#> Searching an str(valud) in KBs"
    print json.dumps(glpi.search('knowbase', criteria),
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)


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

    # test_profile()
    # test_ticket()
    #test_kb()
    # test_general()
    #test_general_search()
    test_search()
