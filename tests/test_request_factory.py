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

class TestRequestFactory(object):
  def setup_method(self, method):
    RequestFactory.REQUEST_TYPES = {}

  def test_registration(self):
    class SampleRequest(Request):
      def getRequestType(self):
        return "SampleRequest"
    RequestFactory.registerRequestType(SampleRequest)

    assert SampleRequest == RequestFactory.REQUEST_TYPES["SampleRequest"]

  def test_failedRegistrationNotImplemented(self):
    class SampleBadRequest(Request):
      pass

    try:
      RequestFactory.registerRequestType(SampleBadRequest)
    except NotImplementedError:
      assert True
    else:
      assert False

  def test_failedRegistrationWrongInheritence(self):
    class SampleBadRequest(object):
      pass

    try:
      RequestFactory.registerRequestType(SampleBadRequest)
    except AttributeError:
      assert True
    else:
      assert False

  def test_getRequest(self):
    class SampleRequest(Request):
      def getRequestType(self):
        return "SampleRequest"

      def __init__(self, args = {}, credentials = None):
        pass

    RequestFactory.registerRequestType(SampleRequest)

    request = RequestFactory.getRequest("SampleRequest", {}, None)

    assert "SampleRequest" == request.getRequestType()

  def test_getRequestWrong(self):
    try:
      request = RequestFactory.getRequest("SampleRequest", {}, None)
    except UnknownRequest:
      assert True
    else:
      assert False

  def test_unregistration(self):
    class SampleRequest(Request):
      def getRequestType(self):
        return "SampleRequest"
    RequestFactory.registerRequestType(SampleRequest)

    RequestFactory.unregisterRequestType(SampleRequest)

    try:
      request = RequestFactory.getRequest("SampleRequest", {}, None)
    except UnknownRequest:
      assert True
    else:
      assert False

  def test_unregistrationAgain(self):
    class SampleRequest(Request):
      def getRequestType(self):
        return "SampleRequest"
    RequestFactory.registerRequestType(SampleRequest)

    RequestFactory.unregisterRequestType(SampleRequest)

    try:
      RequestFactory.unregisterRequestType(SampleRequest)
    except UnknownRequest:
      assert True
    else:
      assert False
