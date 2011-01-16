#!/usr/bin/python

#   Copyright 2010-2011 Alexandre Zani (alexandre.zani@gmail.com) 
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
from pod.credentials import *

class RequestFactory(object):
  """ This factory class holds the different available request types and
  generates request objects which can then be executed.
  """
  def __init__(self):
    self.request_types = {}

  def registerRequestType(self, request):
    """ Adds an available request type.
    """
    self.request_types[request.REQUEST_TYPE] = request

  def unregisterRequestType(self, request):
    """ Removes an available request type.
    """
    try:
      del self.request_types[request.REQUEST_TYPE]
    except KeyError:
      raise UnknownRequest("Unknown request: " + request.REQUEST_TYPE)

  def getRequest(self, request_type, args, credentials):
    """ Returns a request object of the corresponding request type
    """
    try:
      request = self.request_types[request_type]
    except KeyError:
      raise UnknownRequest("Unknown request: " + request_type)

    return request(args, credentials)

  def parseRequest(self, request_str, credentials=None, auth_db=None,
      credentials_factory=None):
    try:
      msg = json.loads(request_str)
      request_dict = msg["request"]
    except ValueError:
      raise MalformedRequest(request_str)
    except KeyError:
      raise MalformedRequest(request_str)

    try:
      request_type = request_dict["type"]
    except KeyError:
      raise MissingRequestType(request_str)

    try:
      request_args = request_dict["args"]
    except KeyError:
      request_args = {}

    if credentials == None and credentials_factory != None:
      try:
        credentials_dict = msg["credentials"]
        credentials = credentials_factory.parseCredentials(
            credentials_dict=credentials_dict,
            database=auth_db)
      except KeyError:
        credentials = None

    return self.getRequest(request_type, request_args, credentials)


def abstract():
  import inspect
  caller = inspect.getouterframes(inspect.currentframe())[1][3]
  raise NotImplementedError(caller + ' must be implemented in subclass')

class Request(object):
  """ Requests are generated by the RequestFactory. 
  """
  def getRequestType(self): abstract()

class RequestError(Exception): pass
class UnknownRequest(RequestError): pass
class MalformedRequest(RequestError): pass
class MissingRequestType(MalformedRequest): pass
class MissingRequestArgument(RequestError): pass
