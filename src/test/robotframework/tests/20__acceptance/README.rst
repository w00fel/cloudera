.. default-role:: code

Acceptance Tests
----------------

* `Local Host Acceptance Test <10__local/README.rst>`_
* `Remote Host Acceptance Test <20__remote.rst>`_
* `LCOPY Acceptance Test <30__LCOPY.rst>`_
* `HDFS ACLs Acceptance Test <40__ACLs.rst>`_
* `HDFS Failover Acceptance Test <50__failover.rst>`_

The acceptance tests can be run independently from the smoke tests by using the 'suites'
system property on the maven command line: `mvn -Dsuites=acceptance`
