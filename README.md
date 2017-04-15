# glpi-sdk-python

[![Build Status](https://travis-ci.org/truly-systems/glpi-sdk-python.svg?branch=master)](https://travis-ci.org/truly-systems/glpi-sdk-python)

GLPI SDK written in Python.

## Description

This SDK is written in Python to help developers integrate their apps, APIS
and scripts in GLPI infrastructure. This SDK abstract the [GLPI Rest API](https://github.com/glpi-project/glpi/blob/9.1/bugfixes/apirest.md)

To usage it, you should have username, password and API-Token from your GLPI
server.

See also:
* [GLPI Rest API](https://github.com/glpi-project/glpi/blob/9.1/bugfixes/apirest.md#list-searchoptions)

## SDK supported items

* Ticket: get, get all, create
* Knowledge Base: get, get all, create

## Install

Just install using pip, from:

* Repository:

`pip install -e git+https://github.com/truly-systems/glpi-sdk-python.git@master#egg=glpi`

* requirements.txt

```shell
$ echo '-e git+https://github.com/truly-systems/glpi-sdk-python.git@master#egg=glpi`'\
  > requirements.txt

$ pip install -r requirements.txt
```

## Usage

You should enable the GLPI API and generate an App Token. TO create one follow these steps:

* TODO

Please, change the vars bellow with yours:

```python
username = "GLPI_USER"
password = "GLPI_USER"
url = 'http://glpi.example.com/apirest.php'
glpi_app_token = "GLPI_API_TOKEN"

```

### Tickets

* Get all Tickets

```python
from glpi import GlpiTicket

glpi_ticket = GlpiTicket(url, glpi_app_token,
                         username=username,
                         password=password)

tickets_all = glpi_ticket.get_all()
print "Retrieving all tickets: %s" % json.dumps(tickets_all,
                  indent=4,
                  separators=(',', ': '),
                  sort_keys=True)
```

* Create an Ticket

```python
from glpi import GlpiTicket, Ticket

glpi_ticket = GlpiTicket(url, glpi_app_token,
                       username=username,
                       password=password)

ticket = Ticket(name='New ticket from SDK',
                content='>>>> Content of ticket created by SDK API <<<')

ticket_dict = glpi_ticket.create(ticket_data=ticket)
print "Created the ticket: %s" % ticket_dict

```

* Get ticket by ID

```python
from glpi import GlpiTicket, Ticket

glpi_ticket = GlpiTicket(url, glpi_app_token,
                       username=username,
                       password=password)

ticket_dict = {}
ticket_dict['id'] = 1
ticket_get = glpi_ticket.get(ticket_dict['id'])
print "Got this ticket: %s" % json.dumps(ticket_get,
                  indent=4,
                  separators=(',', ': '),
                  sort_keys=True)

```

* Profile information

```python
from glpi import GlpiProfile

glpi_pfl = GlpiProfile(url,
            glpi_app_token, username=username,
            password=password)

print "Getting profile "
print json.dumps(glpi_pfl.get_my_profiles(),
               indent=4, separators=(',', ': '))
```

* Reusing session token

```python
token_session = glpi_pfl.get_session_token()
print "Update session for Ticket object: %s" %\
        glpi_ticket.update_session_token(token_session)

```

* Full example

```python
from glpi import GlpiProfile
from glpi import GlpiTicket, Ticket


username = "GLPI_USER"
password = "GLPI_USER"
url = 'http://glpi.example.com/apirest.php'
glpi_app_token = "GLPI_API_TOKEN"


if __name__ == '__main__':

  glpi_pfl = GlpiProfile(url,
              glpi_app_token, username=username,
              password=password)

  print "Getting profile "
  print json.dumps(glpi_pfl.get_my_profiles(),
                   indent=4, separators=(',', ': '))

  token_session = glpi_pfl.get_session_token()
  print "Current session is: %s" % token_session

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

  ticket = Ticket(name='New ticket from SDK',
                  content=' Content of ticket created by SDK API ')
  ticket_dict = glpi_ticket.create(ticket_data=ticket)
  print "Created the ticket: %s" % ticket_dict

  print "Getting ticket recently created with id %d ..." % ticket_dict['id']
  ticket_get = glpi_ticket.get(ticket_dict['id'])
  print "Got this ticket: %s" % json.dumps(ticket_get,
                    indent=4,
                    separators=(',', ': '),
                    sort_keys=True)

```

## CONTRIBUTING

### TEST the code

* Install tests dependencies

`make dependencies`

* Test PEP syntax

`make check-syntax`

* Test installation setup

`make test-setup`
