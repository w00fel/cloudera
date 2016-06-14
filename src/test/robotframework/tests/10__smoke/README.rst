.. default-role:: code

Smoke Tests
-----------

These aren't tests of the HDFS URI - this is a test suite which verifies that
the test fixtures behave as expected and performs basic connectivity tests of
the FTP and HDFS servers to verify that the test environment is set up properly.

* `FTP Client Smoke Test <10__FTP.rst>`_
* `HDFS Client Smoke Test <20__HDFS.rst>`_
* `SOAP Client Smoke Test <30__SOAP.rst>`_
* `SSH Client Smoke Test <40__SSH.rst>`_

The smoke tests can be run independently from the acceptance tests by using the 'suites'
system property on the maven command line: `mvn -Dsuites=smoke`
