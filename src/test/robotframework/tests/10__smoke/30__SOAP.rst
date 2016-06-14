SOAP Client Smoke Test
----------------------

Verify that the embedded SOAP client is working as expected and that the
SOAP endpoint is available on the system under test.

The SOAP client is used in the Acceptance Tests to trigger actions on the Harmony server.

.. code:: robotframework

    *** Settings ***
    Documentation  Connectivity Tests for SOAP Client
    Force Tags  Smoke

    Resource  ${test.dir}/common.rst

    *** Test Cases ***
    Get SOAP Version
        [Documentation]  Connect to the SOAP endpoint and get version.
        ${version} =  Get Version
        Set Test Message  ${version}

    *** Keywords ***
    Get Version
        Create Soap Client  ${soap_endpoint}/Version?wsdl
        ${result} =  Call Soap Method  getVersion
        [Return]  ${result}
