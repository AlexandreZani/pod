#!/usr/bin/python

#   Copyright 2010 Alexandre Zani (alexandre.zani@gmail.com) 
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json

class CredentialsFactory(object):
  """ This factory class holds the different available credential
  types and generates credentials object which can then be verified.
  """
  CREDENTIALS_TYPES = {}

  @staticmethod
  def registerCredentialsType(cred_type):
    """ Registers a new credentials type
    """
    CredentialsFactory.CREDENTIALS_TYPES[cred_type.CREDENTIALS_TYPE] = cred_type

  @staticmethod
  def unregisterCredentialsType(cred_type):
    """ Unregisters a credentials type
    """
    try:
      del CredentialsFactory.CREDENTIALS_TYPES[cred_type]
    except KeyError:
      raise UnknownCredentials("Unknown credentials" + cred_type)

  @staticmethod
  def getCredentials(cred_type, args, database):
    """ Gets a credentials object
    """
    try:
      cred_class = CredentialsFactory.CREDENTIALS_TYPES[cred_type]
    except KeyError:
      raise UnknownCredentials("Unknown credentials: " + cred_type)

    return cred_class(args, database)

  @staticmethod
  def parseCredentials(credentials_str, database):
    try:
      credentials_dict = json.loads(credentials_str)["credentials"]
    except ValueError:
      raise MalformedCredentials(credentials_str)
    except KeyError:
      raise MalformedCredentials(credentials_str)

    try:
      credentials_type = credentials_dict["type"]
    except KeyError:
      raise MissingCredentialsType(credentials_str)

    try:
      credentials_args = credentials_dict["args"]
    except KeyError:
      credentials_args = None

    return CredentialsFactory.getCredentials(credentials_type, credentials_args, database)

def abstract():
  import inspect
  caller = inspect.getouterframes(inspect.currentframe())[1][3]
  raise NotImplementedError(caller + ' must be implemented in subclass')

class Credentials():
  pass

class CredentialsError(Exception): pass
class UnknownCredentials(CredentialsError): pass
class InvalidCredentials(CredentialsError): pass
class MalformedCredentials(CredentialsError): pass
class MissingCredentialsType(MalformedCredentials): pass
