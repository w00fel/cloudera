Local Host Acceptance Tests
---------------------------

The local host acceptance tests use a local mailbox on the Harmony server with the inbox and outbox
configured to point to the HDFS filesystem on the Cloudera Cluster.

The tests are broken down into two sets of scenarios:

* `Positive Scenarios <10__positive.rst>`_
* `Negative Scenarios <20__negative.rst>`_

The positive scenarios are concerned with verifying that the HDFS URI functions correctly under normal
operating conditions and tests the following scenarios:

* Uploads/appends/downloads
* Create/remove files/directories
* Folder browsing via cd/ls
* Size/modification time
* Rename files

The negative scenarios are mainly concerned with verifying that the POSIX permissions of files and
directories are honored by the HDFS URI and that it is not possible to access any files or directories
that the HDFS user does not have appropriate permissions for:

* Permssion tests for rwx
* Permssion tests for user/group/other
* Tests for non-existent files/directories
