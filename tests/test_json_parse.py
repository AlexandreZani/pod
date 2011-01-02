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

from pod.requests import *
from pod.credentials import *

class TestRequestJSON:
  def setup_method(self, method):
    RequestFactory.REQUEST_TYPES = {}

    class SampleRequest(Request):
      def getRequestType(self):
        return "SampleRequest"

      def __init__(self, args = {}, credentials = None):
        self.args = args

    RequestFactory.registerRequestType(SampleRequest)

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

    request = RequestFactory.parseRequest(json_str, None)

    assert 1 == int(request.args["first"])
    assert 2 == int(request.args["second"])
    assert "SampleRequest" == request.getRequestType()

  def test_JsonNoArgs(self):
    json_str = """{
      "request": {
         "type": "SampleRequest"
      }
    }
    """

    request = RequestFactory.parseRequest(json_str, None)

    assert "SampleRequest" == request.getRequestType()

  def test_JsonNoRequest(self):
    json_str = """{
      "request": {
      }
    }
    """

    try:
      request = RequestFactory.parseRequest(json_str, None)
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
      request = RequestFactory.parseRequest(json_str, None)
    except MalformedRequest:
      assert True
    else:
      assert False

  def test_JsonNoRequest(self):
    json_str = """{
    }
    """

    try:
      request = RequestFactory.parseRequest(json_str, None)
    except MalformedRequest:
      assert True
    else:
      assert False

class TestCredentialsJSON:
  def setup_method(self, method):
    CredentialsFactory.CREDENTIALS_TYPES = {}

    class SampleCredentials(Credentials):
      CREDENTIALS_TYPE = "SampleCredentials"

      def __init__(self, args = {}, database = None):
        self.args = args

    CredentialsFactory.registerCredentialsType(SampleCredentials)

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

    credentials = CredentialsFactory.parseCredentials(json_str, None)

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

    credentials = CredentialsFactory.parseCredentials(json_str, None)

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
      credentials = CredentialsFactory.parseCredentials(json_str, None)
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
      credentials = CredentialsFactory.parseCredentials(json_str, None)
    except MalformedCredentials:
      assert True
    else:
      assert False

  def test_JsonNoCredentials(self):
    json_str = """{
    }
    """

    try:
      credentials = CredentialsFactory.parseCredentials(json_str, None)
    except MalformedCredentials:
      assert True
    else:
      assert False
