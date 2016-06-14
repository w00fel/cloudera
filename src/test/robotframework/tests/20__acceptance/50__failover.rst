HDFS Failover Acceptance Test
-----------------------------

This test verifies that when a name node failover occurs that the HDFS URI is able to detect the
new primary name node and continue functioning normally.

.. code:: robotframework

    *** Settings ***
    Documentation  HDFS Failover Acceptance Tests
    Force Tags  Failover  Acceptance  Positive

    Resource  ${test.dir}/common.rst

    Suite Setup  Run Keyword  Connect to HDFS  ${dfs_super_user}  ${dfs_mailbox}
    Suite Teardown  Disconnect from HDFS

    Test Setup  Run Keywords
    ...  Connect to FTP  AND
    ...  Setup for tests

    Test Teardown  Run Keywords
    ...  Disconnect from FTP  AND
    ...  Cleanup after tests

    *** Test Cases ***
    HDFS Failover
        [Documentation]  Verify that HDFS failover is supported.
        ...
        ...  Upload a file via the FTP client, initiate a manual failover and then
        ...  very that the file can be downloaded.

        # Setup
        ${active} =  CDH.Get Active Name Node  ${config.cluster.manager}
        Set Test Variable  ${formatted}  <span style="white-space: nowrap;"><b>${active}</b></span>
        Set Test Message  *HTML* Active Name Node was:<br/>${formatted}

        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        FTP.Upload File  ${file}  ${ftp_remote_dir}/data.bin

        # Action
        CDH.HDFS Failover  ${config.cluster.manager}

        # Verification
        ${active} =  CDH.Get Active Name Node  ${config.cluster.manager}
        Set Test Variable  ${formatted}  <span style="white-space: nowrap;"><b>${active}</b></span>
        Set Test Message  <br/>and is now:<br/>${formatted}  append=yes

        FTP.Download File  ${ftp_remote_dir}/data.bin  ${local_tmp_dir}/data.bin
