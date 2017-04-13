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

### Tickets

* Get all Tickets

```python
from glpi import GlpiTicket

glpi_ticket = GlpiTicket(url, glpi_app_token,
                         username=username,
                         password=password)

print "Retrieving all tickets: %s" %\
       glpi_ticket.get_all()
```

* Create an Ticket

```python
from glpi import GlpiTicket, Ticket

glpi_ticket = GlpiTicket(url, glpi_app_token,
                       username=username,
                       password=password)

ticket = Ticket(name='New ticket from SDK',
                content='>>>> Content of ticket created by SDK API <<<')

print "Creating ticket tickets: %s" % glpi_ticket.create(ticket_data=ticket)

```

* Profile information

```python
from glpi import GlpiProfile

print "Getting profile "
print glpi_pfl.get_my_profiles()
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
    print glpi_pfl.get_my_profiles()

    token_session = glpi_pfl.get_session_token()
    print "Current session is: %s" % token_session
    glpi_ticket = GlpiTicket(url, glpi_app_token,
                             username=username,
                             password=password)

    print "Update Ticket object to session: %s" %\
            glpi_ticket.update_session_token(token_session)

    ticket = Ticket(name='New ticket from SDK',
                    content='>>>> Content of ticket created by SDK API <<<')

    print "Creating ticket tickets: %s" % glpi_ticket.create(ticket_data=ticket)

    print "Retrieving all tickets: %s" %\
            glpi_ticket.get_all()

```
