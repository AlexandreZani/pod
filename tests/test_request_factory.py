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

class Testrequest_factory(object):
  def setup_method(self, method):
    global request_factory
    request_factory = RequestFactory()

  def test_registration(self):
    class SampleRequest(Request):
      REQUEST_TYPE = "SampleRequest"
    request_factory.registerRequestType(SampleRequest)

    assert SampleRequest == request_factory.request_types["SampleRequest"]

  def test_failedRegistrationNotImplemented(self):
    class SampleBadRequest(Request):
      pass

    try:
      request_factory.registerRequestType(SampleBadRequest)
    except AttributeError:
      assert True
    else:
      assert False

  def test_failedRegistrationWrongInheritence(self):
    class SampleBadRequest(object):
      pass

    try:
      request_factory.registerRequestType(SampleBadRequest)
    except AttributeError:
      assert True
    else:
      assert False

  def test_getRequest(self):
    class SampleRequest(Request):
      REQUEST_TYPE = "SampleRequest"

      def __init__(self, args = {}, credentials = None):
        pass

    request_factory.registerRequestType(SampleRequest)

    request = request_factory.getRequest("SampleRequest", {}, None)

    assert "SampleRequest" == request.REQUEST_TYPE

  def test_getRequestWrong(self):
    try:
      request = request_factory.getRequest("SampleRequest", {}, None)
    except UnknownRequest:
      assert True
    else:
      assert False

  def test_unregistration(self):
    class SampleRequest(Request):
      REQUEST_TYPE = "SampleRequest"
    request_factory.registerRequestType(SampleRequest)

    request_factory.unregisterRequestType(SampleRequest)

    try:
      request = request_factory.getRequest("SampleRequest", {}, None)
    except UnknownRequest:
      assert True
    else:
      assert False

  def test_unregistrationAgain(self):
    class SampleRequest(Request):
      REQUEST_TYPE = "SampleRequest"

    request_factory.registerRequestType(SampleRequest)

    request_factory.unregisterRequestType(SampleRequest)

    try:
      request_factory.unregisterRequestType(SampleRequest)
    except UnknownRequest:
      assert True
    else:
      assert False
