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

from pod.requests import *
from pod.credentials import *

class TestRequestJSON:
  def setup_method(self, method):
    global credentials_factory
    credentials_factory = CredentialsFactory()
    global request_factory
    request_factory = RequestFactory()

    class SampleCredentials(Credentials):
      CREDENTIALS_TYPE = "SampleCredentials"

      def __init__(self, args = {}, database = None):
        self.args = args

    credentials_factory.registerCredentialsType(SampleCredentials)

    class SampleRequest(Request):
      REQUEST_TYPE = "SampleRequest"

      def __init__(self, args = {}, credentials = None):
        self.args = args
        self.credentials = credentials

    request_factory.registerRequestType(SampleRequest)

  def test_Json(self):
    json_str = """{
      "request": {
         "type": "SampleRequest",
         "args": {
           "first": "1",
           "second": "2"
        }
      }
    }
    """

    request = request_factory.parseRequest(json_str, None)

    assert 1 == int(request.args["first"])
    assert 2 == int(request.args["second"])
    assert "SampleRequest" == request.REQUEST_TYPE

  def test_JsonEmbededCreds(self):
    json_str = """{
      "request": {
         "type": "SampleRequest",
         "args": {
           "first": "1",
           "second": "2"
        }
      },
      "credentials": {
         "type": "SampleCredentials",
         "args": {
           "first": "1",
           "second": "2"
        }
      }
    }
    """

    request = request_factory.parseRequest(json_str, None,
        credentials_factory=credentials_factory)
    credentials = request.credentials

    assert 1 == int(credentials.args["first"])
    assert 2 == int(credentials.args["second"])
    assert "SampleCredentials" == credentials.CREDENTIALS_TYPE

    assert 1 == int(request.args["first"])
    assert 2 == int(request.args["second"])
    assert "SampleRequest" == request.REQUEST_TYPE

  def test_JsonNoArgs(self):
    json_str = """{
      "request": {
         "type": "SampleRequest"
      }
    }
    """

    request = request_factory.parseRequest(json_str, None)

    assert "SampleRequest" == request.REQUEST_TYPE

  def test_JsonNoRequest(self):
    json_str = """{
      "request": {
      }
    }
    """

    try:
      request = request_factory.parseRequest(json_str, None)
    except MissingRequestType:
      assert True
    else:
      assert False
  
  def test_JsonMalformed(self):
    json_str = """
      "request": {
         "type": "SampleRequest",
         "args": {
           "first": "1",
           "second": "2"
        }
      }
    }
    """

    try:
      request = request_factory.parseRequest(json_str, None)
    except MalformedRequest:
      assert True
    else:
      assert False

  def test_JsonNoRequest(self):
    json_str = """{
    }
    """

    try:
      request = request_factory.parseRequest(json_str, None)
    except MalformedRequest:
      assert True
    else:
      assert False

class TestCredentialsJSON:
  def setup_method(self, method):
    credentials_factory.credentials_types = {}

    class SampleCredentials(Credentials):
      CREDENTIALS_TYPE = "SampleCredentials"

      def __init__(self, args = {}, database = None):
        self.args = args

    credentials_factory.registerCredentialsType(SampleCredentials)

  def test_Json(self):
    json_str = """{
      "credentials": {
         "type": "SampleCredentials",
         "args": {
           "first": "1",
           "second": "2"
        }
      }
    }
    """

    credentials = credentials_factory.parseCredentials(json_str, None)

    assert 1 == int(credentials.args["first"])
    assert 2 == int(credentials.args["second"])
    assert "SampleCredentials" == credentials.CREDENTIALS_TYPE

  def test_JsonNoArgs(self):
    json_str = """{
      "credentials": {
         "type": "SampleCredentials"
      }
    }
    """

    credentials = credentials_factory.parseCredentials(json_str, None)

    assert "SampleCredentials" == credentials.CREDENTIALS_TYPE

  def test_JsonNoType(self):
    json_str = """{
      "credentials": {
         "args": {
           "first": "1",
           "second": "2"
        }
      }
    }
    """

    try:
      credentials = credentials_factory.parseCredentials(json_str, None)
    except MissingCredentialsType:
      assert True
    else:
      assert False

  def test_JsonMalformed(self):
    json_str = """
      "credentials": {
         "type": "SampleCredentials",
         "args": {
           "first": "1",
           "second": "2"
        }
      }
    }
    """

    try:
      credentials = credentials_factory.parseCredentials(json_str, None)
    except MalformedCredentials:
      assert True
    else:
      assert False

  def test_JsonNoCredentials(self):
    json_str = """{
    }
    """

    try:
      credentials = credentials_factory.parseCredentials(json_str, None)
    except MalformedCredentials:
      assert True
    else:
      assert False
