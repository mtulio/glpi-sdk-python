# This is a big script to test some SDK items.

from __future__ import print_function

import os
import json
import time
import pytest
from dotenv import load_dotenv, find_dotenv
from glpi import GlpiProfile
from glpi import GlpiTicket, Ticket
from glpi import GlpiKnowBase, KnowBase
from glpi import GLPI


def load_from_vcap_services(service_name):
    load_dotenv(find_dotenv())
    vcap_services = os.getenv("VCAP_SERVICES")
    if vcap_services is not None:
        services = json.loads(vcap_services)
        if service_name in services:
            return services[service_name][0]["credentials"]
    else:
        return None


@pytest.mark.skipif('VCAP_SERVICES' not in os.environ, reason='disabled because it needs an actual server')
def test_profile(glpi_profile):
    print("Getting profile ")
    print(json.dumps(glpi_profile.get_my_profiles(),
                     indent=4, separators=(',', ': ')))

    token_session = glpi_profile.get_session_token()
    print("Current session is: %s" % token_session)


@pytest.mark.skipif('VCAP_SERVICES' not in os.environ, reason='disabled because it needs an actual server')
def test_ticket(glpi_ticket, timestamp):
    print("##> Update Ticket object to session: %s" %
          glpi_ticket.update_session_token(""))

    tickets_all = glpi_ticket.get_all()
    print("Retrieving all tickets: %s" % json.dumps(tickets_all,
          indent=4,
          separators=(',', ': '),
          sort_keys=True))

    ticket = Ticket(name="New ticket from SDK %s" % timestamp,
                    content=" Content of ticket created by SDK API  %s" % timestamp)
    ticket_dict = glpi_ticket.create(ticket.get_data())
    print("Created the ticket: %s" % ticket_dict)

    print("Getting ticket recently created with id %d ..." % ticket_dict['id'])
    ticket_get = glpi_ticket.get(ticket_dict['id'])
    print("Got this ticket: %s" % json.dumps(ticket_get,
          indent=4,
          separators=(',', ': '),
          sort_keys=True))


@pytest.mark.skipif('VCAP_SERVICES' not in os.environ, reason='disabled because it needs an actual server')
def test_kb(glpi_know_base):
    res = glpi_know_base.get_all()
    print("Retrieving all KBs: %s" % json.dumps(res,
          indent=4,
          separators=(',', ': '),
          sort_keys=True))

    res = glpi_know_base.get(1)
    print("Retrieve KB ID: %s" % json.dumps(res,
          indent=4,
          separators=(',', ': '),
          sort_keys=True))

    kb = KnowBase()
    print("Print default KB: %s" % kb.get_attribute('id'))
    if res is not None:
        kb.set_attributes(res)
    print("Print default KB: %s" % kb.get_attribute('id'))
    print("Retrieving all KBs: %s" % json.dumps(kb.get_stream(),
          indent=4,
          separators=(',', ': '),
          sort_keys=True))

    print("SDK Version: %s" % glpi_know_base.get_version())
    print("SDK Version: %s" % glpi_know_base.__version__)

    print("KB Creating new one...")
    name = "New KB Title %s" % timestamp
    subject = "New KB Body %s" % timestamp
    kb2 = KnowBase()
    kb2.set_attribute('name', name)
    kb2.set_attribute('answer', subject)
    res = kb2.get_attributes()
    print("Retrieving KB obj: %s" % json.dumps(res,
          indent=4,
          separators=(',', ': '),
          sort_keys=True))

    kb_dict = glpi_know_base.create(kb2.get_data())
    print("Creating: %s " % kb_dict)


@pytest.mark.skipif('VCAP_SERVICES' not in os.environ, reason='disabled because it needs an actual server')
def test_general(glpi):
    # Basic usage
    print("#> Getting help()")
    print(glpi.help_item())

    print("#> Getting standard items: ticket")
    print(json.dumps(glpi.get_all('ticket'),
                     indent=4,
                     separators=(',', ': '),
                     sort_keys=True))

    print("#> Setting up new items...")
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
    print("#> Getting new item: COMPUTER")
    print(json.dumps(glpi.get_all('computer'),
                     indent=4,
                     separators=(',', ': '),
                     sort_keys=True))

    # Setting up new map
    print("#####> Creating new MAP...")
    new_map = {
         "knowbase": "/knowbaseitem"
    }
    glpi.set_item_map(new_map)

    print("#> Getting item: KB")
    print(json.dumps(glpi.get_all('knowbase'),
                     indent=4,
                     separators=(',', ': '),
                     sort_keys=True))

    print("#> Getting item KB by ID 1")
    kb_dict = glpi.get('knowbase', 1)
    print(json.dumps(kb_dict,
                     indent=4,
                     separators=(',', ': '),
                     sort_keys=True))
    print(kb_dict)
    print("#> Creating new KB copying from previous...")
    kb_data = {
        "name": "New KB copyied from ID %s at %s" % (
                                        kb_dict['id'], timestamp),
        "answer": "Description of KB: \n <br> API Desc </br> Just a test ",
        "is_faq": kb_dict['is_faq'],
        "knowbaseitemcategories_id": kb_dict['knowbaseitemcategories_id'],
        "users_id": kb_dict['users_id'],
        "view": kb_dict['view']
    }
    print("Creating object data: %s" % repr(kb_data))
    kb_res = glpi.create('knowbase', kb_data)
    print(json.dumps(kb_res,
                     indent=4,
                     separators=(',', ': '),
                     sort_keys=True))


@pytest.mark.skipif('VCAP_SERVICES' not in os.environ, reason='disabled because it needs an actual server')
def test_general_search(glpi):
    print("#> Getting help()")
    print(glpi.help_item())

    print(glpi.init_item('listSearchOptions'))

    token_session = glpi.api_session
    print(">>>> Current session is: %s" % token_session)

    print("#> Getting search options")
    print(json.dumps(glpi.search_options('knowbaseitem'),
                     indent=4,
                     separators=(',', ': '),
                     sort_keys=True))


@pytest.mark.skipif('VCAP_SERVICES' not in os.environ, reason='disabled because it needs an actual server')
def test_search(glpi):
    criteria = {"criteria": [{"field": "name", "value": "portal"}]}
    print("#> Searching an str(valud) in KBs")
    print(json.dumps(glpi.search('knowbase', criteria),
                     indent=4,
                     separators=(',', ': '),
                     sort_keys=True))


@pytest.mark.skipif('VCAP_SERVICES' not in os.environ, reason='disabled because it needs an actual server')
def test_update(glpi):
    item_data = {"id": 60, "name": "[test] Updating an ticket 2"}
    print("#> Updating item 'ticket' with %s" % str(item_data))
    print(json.dumps(glpi.update('ticket', item_data),
                     indent=4,
                     separators=(',', ': '),
                     sort_keys=True))


@pytest.mark.skip(reason='disabled because it needs an actual server')
def test_delete(glpi):
    item_id = 63
    print("#> Deleting item 'ticket' with ID %d" % item_id)
    assert(glpi.delete('ticket', item_id))


@pytest.fixture()
def glpi(service_credentials):
    return GLPI(*service_credentials)


@pytest.fixture()
def glpi_know_base(service_credentials):
    return GlpiKnowBase(*service_credentials)


@pytest.fixture()
def glpi_ticket(service_credentials):
    return GlpiTicket(*service_credentials)


@pytest.fixture()
def glpi_profile(service_credentials):
    return GlpiProfile(*service_credentials)


@pytest.fixture()
def service_credentials():
    vcap_service_credentials = load_from_vcap_services('glpi')

    if vcap_service_credentials is not None and isinstance(
       vcap_service_credentials, dict):
        url = vcap_service_credentials['url']
        username = vcap_service_credentials['username']
        password = vcap_service_credentials['password']
        app_token = vcap_service_credentials['app_token']
        return (url, app_token, (username, password))
    else:
        pytest.fail("Unable to load .env file."
                    "Please create using tests/.env.sample")


@pytest.fixture()
def timestamp():
    return time.strftime("%Y/%m/%d-%H:%M:%S")
