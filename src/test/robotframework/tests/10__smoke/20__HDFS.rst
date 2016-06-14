HDFS Client Smoke Test
----------------------

Verify that the embedded HDFS client is working as expected and that there
is connectivity to the Cloudera Hadoop system.

These tests communicate directly with the HDFS server, bypassing the HDFS URI entirely.

.. code:: robotframework

    *** Settings ***
    Documentation  Connectivity Tests for HDFS Client
    Force Tags  Smoke

    Resource  ${test.dir}/common.rst

    *** Test Cases ***
    Connect to server
        [Documentation]  Connect to the HDFS server.

        ${current_time} =  TestUtils.Get Timestamp
        Set Suite Variable  ${timestamp}  ${current_time}
        Set Suite Variable  ${remote_dir}  /user/${timestamp}

        ${dfs_server} =  CDH.Get Active Name Node  ${config.cluster.manager}
        HDFS.Connect  ${dfs_server}  ${dfs_port}  ${kerberos}  ${dfs_superuser}  ${password}

    Create a new directory
        [Documentation]  Create a test directory to work in.

        HDFS.Create Directory  ${remote_dir}
        HDFS.Set Owner  ${remote_dir}  ${dfs_owner}  ${dfs_group}

    Upload some files
        [Documentation]  Upload some test files.

        # Setup
        ${local_size_1} =  OS.Get File Size  ${data.dir}/${bacon}
        ${local_size_2} =  OS.Get File Size  ${data.dir}/${eggs}
        ${local_size_3} =  OS.Get File Size  ${data.dir}/${spam}

        # Action
        HDFS.Upload File  ${data.dir}/${bacon}  ${remote_dir}/${bacon}
        HDFS.Upload File  ${data.dir}/${eggs}  ${remote_dir}/${eggs}
        HDFS.Upload File  ${data.dir}/${spam}  ${remote_dir}/${spam}

        # Verify
        ${remote_size_1} =  HDFS.Get File Size  ${remote_dir}/${bacon}
        ${remote_size_2} =  HDFS.Get File Size  ${remote_dir}/${eggs}
        ${remote_size_3} =  HDFS.Get File Size  ${remote_dir}/${spam}

        Should Be Equal As Integers  ${local_size_1}  ${remote_size_1}
        Should Be Equal As Integers  ${local_size_2}  ${remote_size_2}
        Should Be Equal As Integers  ${local_size_3}  ${remote_size_3}

    List the directory contents
        [Documentation]  List the test files.

        # Action
        @{directory_list} =  HDFS.List Directory  ${remote_dir}

        # Verify
        Should Contain  @{directory_list}[0]  ${bacon}
        Should Contain  @{directory_list}[1]  ${eggs}
        Should Contain  @{directory_list}[2]  ${spam}

    Rename a file
        [Documentation]  Rename one of the test files.

        # Action
        HDFS.Rename File  ${remote_dir}/${bacon}  ${remote_dir}/${sausage}

        # Verify
        @{directory_list} =  HDFS.List Directory  ${remote_dir}
        Should Contain  @{directory_list}[1]  ${sausage}

    Set/Get the file modification time
        [Documentation]  Set/get the file modification time.

        # Action
        HDFS.Set Modified Time  ${remote_dir}/${sausage}  ${timestamp}
        ${modified_time} =  HDFS.Get Modified Time  ${remote_dir}/${sausage}

        # Verify
        Should Be Equal As Integers  ${modified_time}  ${timestamp}

    List the directory file names
        [Documentation]  List the test file names.

        # Action
        @{directory_list} =  HDFS.List Files In Directory  ${remote_dir}

        # Verify
        Should Be Equal  @{directory_list}[0]  ${eggs}
        Should Be Equal  @{directory_list}[1]  ${sausage}
        Should Be Equal  @{directory_list}[2]  ${spam}

    Remove a directory
        [Documentation]  Create/remove a new directory.

        # Setup
        HDFS.Create Directory  ${remote_dir}/${squeamish}

        # Action
        HDFS.Remove Directory  ${remote_dir}/${squeamish}

        # Verify
        @{directory_list} =  HDFS.List Directory  ${remote_dir}
        Should Not Contain  @{directory_list}  ${squeamish}

    Delete some files
        [Documentation]  Delete some of the test files.

        # Action
        HDFS.Remove File  ${remote_dir}/${eggs}
        HDFS.Remove File  ${remote_dir}/${spam}

        # Verify
        @{directory_list} =  HDFS.List Directory  ${remote_dir}
        Should Not Contain  @{directory_list}  ${eggs}
        Should Not Contain  @{directory_list}  ${spam}

    Download a file
        [Documentation]  Retrieve the final remaining test file.

        # Setup
        ${remote_size} =  HDFS.Get File Size  ${remote_dir}/${sausage}
        ${local_tmp} =  TestUtils.Create Temp Directory

        # Action
        HDFS.Download File  ${remote_dir}/${sausage}  ${local_tmp}/${sausage}

        # Verify
        ${local_size} =  OS.Get File Size  ${local_tmp}/${sausage}
        Should Be Equal As Integers  ${local_size}  ${remote_size}

        # Cleanup
        OS.Remove Directory  ${local_tmp}  recursive=yes

    Suite Cleanup
        [Documentation]  Cleanup any remaining local/remote test files/directories.

        HDFS.Remove Directory  ${remote_dir}
        OS.Remove File  ${sausage}
        HDFS.Close
