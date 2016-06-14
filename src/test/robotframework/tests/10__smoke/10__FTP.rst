FTP Client Smoke Test
---------------------

Verify that the embedded FTP client is working as expected and that there
is connectivity to the system under test.

These tests use a local FTP user and do not interact with the HDFS URI.

.. code:: robotframework

    *** Settings ***
    Documentation  Connectivity Tests for FTP Client
    Force Tags  Smoke

    Resource  ${test.dir}/common.rst

    *** Variables ***
    ${ftp_login}  dan

    *** Test Cases ***
    Connect to server
        [Documentation]  Connect to the FTP server.
        ...  Invokes the USER/PASS commands.

        ${timestamp} =  TestUtils.Get Timestamp
        Set Suite Variable  ${remote_dir}  /${timestamp}

        FTP.Connect  ${ftp_server}  ${ftp_port}  ${ftp_login}  ${ftp_password}

    Ask for help
        [Documentation]  Invokes the HELP/SITE commands.

        FTP.Send Command  HELP
        FTP.Send Command  SITE HELP

    Get the remote system type
        [Documentation]  Invokes the SYST command.

        FTP.Send Command  SYST

    Get the remote system status
        [Documentation]  Invokes the STAT command.

        FTP.Send Command  STAT

    Switch to Binary transfer mode
        [Documentation]  Invokes the TYPE command.

        FTP.Send Command  TYPE I

    Slack off for a while
        [Documentation]  Invokes the NOOP command.

        FTP.Send Command  NOOP

    Create a new directory
        [Documentation]  Invokes the MKD command.

        FTP.Create Directory  ${remote_dir}

    Change working directory
        [Documentation]  Invokes the CWD/PWD commands.

        # Action
        FTP.Change Directory  ${remote_dir}

        # Verify
        ${result} =  FTP.Get Current Directory
        Should Be Equal  ${result}  ${remote_dir}

    Upload some files
        [Documentation]  Invokes the STOR/SIZE commands.

        # Setup
        ${local_size_1} =  OS.Get File Size  ${data.dir}/${bacon}
        ${local_size_2} =  OS.Get File Size  ${data.dir}/${eggs}
        ${local_size_3} =  OS.Get File Size  ${data.dir}/${spam}

        # Action
        FTP.Upload File  ${data.dir}/${bacon}
        FTP.Upload File  ${data.dir}/${eggs}
        FTP.Upload File  ${data.dir}/${spam}

        # Verify
        ${remote_size_1} =  FTP.Get File Size  ${bacon}
        ${remote_size_2} =  FTP.Get File Size  ${eggs}
        ${remote_size_3} =  FTP.Get File Size  ${spam}

        Should Be Equal As Integers  ${local_size_1}  ${remote_size_1}
        Should Be Equal As Integers  ${local_size_2}  ${remote_size_2}
        Should Be Equal As Integers  ${local_size_3}  ${remote_size_3}

    Append to a file
        [Documentation]  Invokes the APPE command.

        # Setup
        ${local_size_1} =  OS.Get File Size  ${data.dir}/${bacon}
        ${local_size_2} =  OS.Get File Size  ${data.dir}/${eggs}
        ${expected_size} =  Evaluate  ${local_size_1} + ${local_size_2}

        # Action
        FTP.Append To File  ${data.dir}/${eggs}  ${bacon}

        # Verify
        ${appended_size} =  FTP.Get File Size  ${bacon}
        Should Be Equal As Integers  ${expected_size}  ${appended_size}

    List the directory contents
        [Documentation]  Invokes the LIST command.

        # Action
        @{directory_list} =  FTP.List Directory

        # Verify
        Should Contain  @{directory_list}[0]  ${bacon}
        Should Contain  @{directory_list}[1]  ${eggs}
        Should Contain  @{directory_list}[2]  ${spam}

    Rename a file
        [Documentation]  Invokes the RNFR/RNTO commands.

        # Action
        FTP.Rename File  ${bacon}  ${sausage}

        # Verify
        @{directory_list} =  FTP.List Directory
        Should Contain  @{directory_list}[1]  ${sausage}

    Get the file modification time
        [Documentation]  Invokes the MDTM command.

        # Action
        ${modtime} =  FTP.Get Modified Time  ${sausage}

    List the directory file names
        [Documentation]  Invokes the NLST command.

        # Action
        @{directory_list} =  FTP.List Files In Directory

        # Verify
        Should Be Equal  @{directory_list}[0]  ${eggs}
        Should Be Equal  @{directory_list}[1]  ${sausage}
        Should Be Equal  @{directory_list}[2]  ${spam}

    Remove a directory
        [Documentation]  Invokes the RMD command.

        # Setup
        FTP.Create Directory  ${squeamish}

        # Action
        FTP.Remove Directory  ${squeamish}

        # Verify
        @{directory_list} =  FTP.List Directory
        Should Not Contain  @{directory_list}  ${squeamish}

    Delete some files
        [Documentation]  Invokes the DELE command.

        # Action
        FTP.Remove File  ${eggs}
        FTP.Remove File  ${spam}

        # Verify
        @{directory_list} =  FTP.List Directory
        Should Not Contain  @{directory_list}  ${eggs}
        Should Not Contain  @{directory_list}  ${spam}

    Download a file
        [Documentation]  Invokes the RETR command.

        # Setup
        ${remote_size} =  FTP.Get File Size  ${sausage}
        ${local_tmp} =  TestUtils.Create Temp Directory

        # Action
        FTP.Download File  ${sausage}  ${local_tmp}/${sausage}

        # Verify
        ${local_size} =  OS.Get File Size  ${local_tmp}/${sausage}
        Should Be Equal As Integers  ${local_size}  ${remote_size}

        # Cleanup
        OS.Remove Directory  ${local_tmp}  recursive=yes

    Change back to root directory
        [Documentation]  Invokes the CDUP command.

        # Action
        FTP.Send Command  CDUP

        # Verify
        ${result} =  FTP.Get Current Directory
        Should Be Equal  ${result}  /

    Suite Cleanup
        [Documentation]  Invokes the QUIT command.

        # Clean up test nuggets
        FTP.Remove File  ${remote_dir}/${sausage}
        FTP.Remove Directory  ${remote_dir}

        # Buh-Bye!
        FTP.Close
