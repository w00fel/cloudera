SSH Client Smoke Test
---------------------

Verify that the embedded SSH client is working as expected and that the
SSH server is available on the system under test.

The SSH client is used during test setup in the Acceptance Tests to transfer
test data to/from the Harmony server.

.. code:: robotframework

    *** Settings ***
    Documentation  Connectivity Tests for SSH Client
    Force Tags  Smoke

    Resource  ${test.dir}/common.rst

    *** Test Cases ***
    Connect to server
        [Documentation]  Connect to the SSH server and log welcome message.

        ${timestamp} =  TestUtils.Get Timestamp
        Set Suite Variable  ${remote_dir}  /tmp/${timestamp}

        ${message} =  SSH.Connect  ${ssh_server}  ${ssh_port}  ${ssh_login}  ${ssh_key}
        Set Test Message  ${message}

    Upload some files
        [Documentation]  Upload some test files.

        # Setup
        ${local_size_1} =  OS.Get File Size  ${data.dir}/${bacon}
        ${local_size_2} =  OS.Get File Size  ${data.dir}/${eggs}
        ${local_size_3} =  OS.Get File Size  ${data.dir}/${spam}

        # Action
        SSH.Upload File  ${data.dir}/${bacon}  ${remote_dir}/${bacon}
        SSH.Upload File  ${data.dir}/${eggs}  ${remote_dir}/${eggs}
        SSH.Upload File  ${data.dir}/${spam}  ${remote_dir}/${spam}

        # Verify
        ${remote_size_1} =  SSH.Get File Size  ${remote_dir}/${bacon}
        ${remote_size_2} =  SSH.Get File Size  ${remote_dir}/${eggs}
        ${remote_size_3} =  SSH.Get File Size  ${remote_dir}/${spam}

        Should Be Equal As Integers  ${local_size_1}  ${remote_size_1}
        Should Be Equal As Integers  ${local_size_2}  ${remote_size_2}
        Should Be Equal As Integers  ${local_size_3}  ${remote_size_3}

    Download some files
        [Documentation]  Download the test files.

        # Setup
        ${local_tmp} =  TestUtils.Create Temp Directory
        ${remote_size_1} =  SSH.Get File Size  ${remote_dir}/${bacon}
        ${remote_size_2} =  SSH.Get File Size  ${remote_dir}/${eggs}
        ${remote_size_3} =  SSH.Get File Size  ${remote_dir}/${spam}

        # Action
        SSH.Download File  ${remote_dir}/*  ${local_tmp}${/}

        # Verify
        ${local_size_1} =  OS.Get File Size  ${local_tmp}/${bacon}
        ${local_size_2} =  OS.Get File Size  ${local_tmp}/${eggs}
        ${local_size_3} =  OS.Get File Size  ${local_tmp}/${spam}

        Should Be Equal As Integers  ${local_size_1}  ${remote_size_1}
        Should Be Equal As Integers  ${local_size_2}  ${remote_size_2}
        Should Be Equal As Integers  ${local_size_3}  ${remote_size_3}

        # Cleanup
        OS.Remove Directory  ${local_tmp}  recursive=yes

    Suite Cleanup
        [Documentation]  Cleanup any remaining remote test files/directories.

        SSH.Remove Directory  ${remote_dir}
        SSH.Close Connection
