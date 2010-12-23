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

from pod.credentials import *

class TestCredentialsFactory(object):
  def setup_method(self, method):
    CredentialsFactory.CREDENTIALS_TYPES= {}

  def test_register(self):
    class SampleCreds(Credentials):
      def getCredentialsType(self):
        return "SampleCreds"

    CredentialsFactory.registerCredentialsType(SampleCreds)

    assert SampleCreds == CredentialsFactory.CREDENTIALS_TYPES["SampleCreds"]

  def test_registerWrongInheritence(self):
    class SampleCreds(object):
      pass

    try:
      CredentialsFactory.registerCredentialsType(SampleCreds)
    except AttributeError:
      assert True
    else:
      assert False

  def test_registerUnimplementedType(self):
    class SampleCreds(Credentials):
      pass

    try:
      CredentialsFactory.registerCredentialsType(SampleCreds)
    except NotImplementedError:
      assert True
    else:
      assert False

  def test_getCredentials(self):
    class SampleCreds(Credentials):
      def getCredentialsType(self):
        return "SampleCreds"

      def __init__(self, args = {}, database = None):
        pass

    CredentialsFactory.registerCredentialsType(SampleCreds)

    credentials = CredentialsFactory.getCredentials("SampleCreds", {}, None)

    assert "SampleCreds" == credentials.getCredentialsType()

  def test_getCredentialsWrong(self):
    try:
      credentials = CredentialsFactory.getCredentials("SampleCreds", {}, None)
    except UnknownCredentials:
      assert True
    else:
      assert False

  def test_unregister(self):
    class SampleCreds(Credentials):
      def getCredentialsType(self):
        return "SampleCreds"

    CredentialsFactory.registerCredentialsType(SampleCreds)

    CredentialsFactory.unregisterCredentialsType("SampleCreds")

    try:
      credentials = CredentialsFactory.getCredentials("SampleCreds", {}, None)
    except UnknownCredentials:
      assert True
    else:
      assert False

  def test_unregisterAgain(self):
    class SampleCreds(Credentials):
      def getCredentialsType(self):
        return "SampleCreds"

    CredentialsFactory.registerCredentialsType(SampleCreds)

    CredentialsFactory.unregisterCredentialsType("SampleCreds")

    try:
      CredentialsFactory.unregisterCredentialsType("SampleCreds")
    except UnknownCredentials:
      assert True
    else:
      assert False
