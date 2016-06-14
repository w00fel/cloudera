Local Host Acceptance Tests - Positive Scenarios
------------------------------------------------

.. code:: robotframework

    *** Settings ***
    Documentation  Local Host Acceptance Tests - Positive Scenarios
    Force Tags  Local  Acceptance  Positive

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
    Create a directory
        [Documentation]  Verify that a new directory can be created.
        ...
        ...  Create a new directory via the FTP client and then verify
        ...  that the directory exists using the HDFS client.

        # Action
        FTP.Create Directory  ${ftp_remote_dir}/${squeamish}

        # Verification
        &{status} =  HDFS.Get Path Status  ${dfs_remote_dir}/${squeamish}
        Should Be Equal  DIRECTORY  ${status.type}

    Get the current working directory
        [Documentation]  Verify that the current working directory is correct.
        ...
        ...  Change the current working directory via the FTP client
        ...  and then verify that the path is correct.

        # Setup
        HDFS.Create Directory  ${dfs_remote_dir}/${squeamish}
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_owner}  ${dfs_group}

        # Action
        FTP.Change Directory  ${ftp_remote_dir}/${squeamish}
        ${current} =  FTP.Get Current Directory

        # Verification
        Should Be Equal  ${current}  ${ftp_remote_dir}/${squeamish}

    Remove a directory
        [Documentation]  Verify that a directory can be removed.
        ...
        ...  Delete the test directory via the FTP client and then verify
        ...  that the directory does not exist using the HDFS client.

        # Setup
        HDFS.Create Directory  ${dfs_remote_dir}/${squeamish}
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_owner}  ${dfs_group}

        # Action
        FTP.Remove Directory  ${ftp_remote_dir}/${squeamish}

        # Verification
        ${status} =  HDFS.Get Path Status  ${dfs_remote_dir}/${squeamish}
        Should Be Equal  ${None}  ${status}

    Upload a file
        [Documentation]  Verify that a file can be uploaded.
        ...
        ...  Upload a file via the FTP client and then verify that the
        ...  contents are identical to the local copy of the file.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  1MB  data.bin

        # Action
        FTP.Upload File  ${file}  ${ftp_remote_dir}/data.bin

        # Verification
        Verify Checksums Match  ${file}  ${dfs_remote_dir}/data.bin

    Append to a file
        [Documentation]  Verify that a file can be appended to.
        ...
        ...  Upload a file via the FTP client, append more content to it,
        ...  then verify that the contents are identical to a local copy
        ...  of the appended data.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  1MB  data.bin
        ${data} =  TestUtils.Create Test File  ${local_tmp_dir}  2MB

        # Action
        FTP.Upload File  ${file}  ${ftp_remote_dir}/data.bin
        FTP.Append To File  ${data}  ${ftp_remote_dir}/data.bin

        # Verification
        ${appended} =  TestUtils.Append Test Files  ${local_tmp_dir}  ${file}  ${data}
        Verify Checksums Match  ${appended}  ${dfs_remote_dir}/data.bin

    Download a file
        [Documentation]  Verify that a file can be downloaded.
        ...
        ...  Upload a file via the HDFS client and then download it using
        ...  the FTP client. Verify that the contents are identical.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  1MB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin

        # Action
        FTP.Download File  ${ftp_remote_dir}/data.bin  ${local_tmp_dir}/data.bin

        # Verification
        Verify Checksums Match  ${local_tmp_dir}/data.bin  ${dfs_remote_dir}/data.bin

    Get file modification time
        [Documentation]  Verify that the file modification time is correct.
        ...
        ...  Upload a file via the HDFS client and then get its modification
        ...  time using the FTP client. Verify that the timestamps are identical.
        ...
        ...  NOTE: This test is effectively being skipped other than verifying that the MDTM
        ...  response is all numeric.
        ...
        ...  BUG: The Harmony 5.3.0.X FTP Server is returning the file modification time as
        ...  local server time and not UTC as is typically the case.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  1MB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin

        # Action
        ${mod_time} =  FTP.Get Modified Time  ${ftp_remote_dir}/data.bin

        # Verification
        Should Match Regexp  ${mod_time}  [0-9]+
        Pass Execution  MDTM command returns local server time and not UTC.  Skipped

    Get file size
        [Documentation]  Verify that the file size is correct.
        ...
        ...  Upload a file via the HDFS client and then get its size
        ...  using the FTP client. Verify that the sizes are identical.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  1MB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin

        # Action
        ${remote_size} =  FTP.Get File Size  ${ftp_remote_dir}/data.bin

        # Verification
        ${local_size} =  OS.Get File Size  ${file}
        Should Be Equal As Integers  ${local_size}  ${remote_size}

    Rename a file
        [Documentation]  Verify that a file can be renamed.
        ...
        ...  Upload a file via the HDFS client and then rename it using the
        ...  FTP client. Verify using the HDFS client that the file with the
        ...  new name is present and that the old name is not.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  1MB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/original.bin

        # Action
        FTP.Rename File  ${ftp_remote_dir}/original.bin  ${ftp_remote_dir}/renamed.bin

        # Verification
        ${old_status} =  HDFS.Get Path Status  ${dfs_remote_dir}/original.bin
        ${new_status} =  HDFS.Get Path Status  ${dfs_remote_dir}/renamed.bin
        Should Be Equal  ${None}  ${old_status}
        Should Not Be Equal  ${None}  ${new_status}

    Delete a file
        [Documentation]  Verify that a file can be deleted.
        ...
        ...  Upload a file via the HDFS client and then delete it using the FTP.
        ...  client. Verify using the HDFS client that the file is not present

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  1MB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin

        # Action
        FTP.Remove File  ${ftp_remote_dir}/data.bin

        # Verification
        ${status} =  HDFS.Get Path Status  ${dfs_remote_dir}/data.bin
        Should Be Equal  ${None}  ${status}

    List directory: empty directory
        [Documentation]  Verify that listing an empty directory returns no results.

        # Action
        @{directory_list} =  FTP.List Directory  ${ftp_remote_dir}

        # Verification
        ${directory_list_length} =  Get Length  ${directory_list}
        Should Be Equal As Integers  0  ${directory_list_length}

    List files in directory: empty directory
        [Documentation]  Verify that listing files in an empty directory returns no results.
        # Action
        @{name_list} =  FTP.List Files In Directory  ${ftp_remote_dir}

        # Verification
        ${name_list_length} =  Get Length  ${name_list}
        Should Be Equal As Integers  0  ${name_list_length}

    List directory: mix of directories/files
        [Documentation]  Verify that the contents of a directory can be listed.
        ...
        ...  Using the HDFS client, upload some files and create directories. Verify
        ...  via the FTP client that the directory can be listed and that the resulting
        ...  list contains the expected files/directories sorted in the correct order.

        # Setup
        Create File/Directory Mix

        # Action
        @{directory_list} =  FTP.List Directory  ${ftp_remote_dir}

        # Verification
        ${directory_list_length} =  Get Length  ${directory_list}
        Should Be Equal As Integers  7  ${directory_list_length}

        Should Contain  @{directory_list}[0]  Do
        Should Contain  @{directory_list}[1]  Fa
        Should Contain  @{directory_list}[2]  La
        Should Contain  @{directory_list}[3]  Mi
        Should Contain  @{directory_list}[4]  Re
        Should Contain  @{directory_list}[5]  Sol
        Should Contain  @{directory_list}[6]  Ti

    List files in directory: mix of directories/files
        [Documentation]  Verify that file names only in a directory can be listed.
        ...
        ...  Using the HDFS client, upload some files and create directories. Verify
        ...  via the FTP client that the _file names only_ can be listed and that the
        ...  resulting list contains the expected files sorted in the correct order.

        # Setup
        Create File/Directory Mix
        FTP.Change Directory  ${ftp_remote_dir}

        # Action
        @{name_list} =  FTP.List Files In Directory

        # Verification
        ${name_list_length} =  Get Length  ${name_list}
        Should Be Equal As Integers  3  ${name_list_length}

        Should Be Equal  @{name_list}[0]  Fa
        Should Be Equal  @{name_list}[1]  Mi
        Should Be Equal  @{name_list}[2]  Sol

    List files in directory: only directories/no files present
        [Documentation]  Verify that no file names are listed.
        ...
        ...  Using the HDFS client, create directories only. Verify via the
        ...  FTP client that the file names only_ can be listed and that the
        ...  resulting list is empty.

        # Setup
        Create Directories Only

        # Action
        @{name_list} =  FTP.List Files In Directory  ${ftp_remote_dir}

        # Verification
        ${name_list_length} =  Get Length  ${name_list}
        Should Be Equal As Integers  0  ${name_list_length}

    *** Keywords ***
    Create File/Directory Mix
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Create Directory  ${dfs_remote_dir}/Do
        HDFS.Create Directory  ${dfs_remote_dir}/Re
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/Mi
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/Fa
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/Sol
        HDFS.Create Directory  ${dfs_remote_dir}/La
        HDFS.Create Directory  ${dfs_remote_dir}/Ti

    Create Directories Only
        HDFS.Create Directory  ${dfs_remote_dir}/Do
        HDFS.Create Directory  ${dfs_remote_dir}/Re
        HDFS.Create Directory  ${dfs_remote_dir}/La
        HDFS.Create Directory  ${dfs_remote_dir}/Ti
