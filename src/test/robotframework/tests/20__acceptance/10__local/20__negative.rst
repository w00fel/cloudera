Local Host Acceptance Tests - Negative Scenarios
------------------------------------------------

.. code:: robotframework

    *** Settings ***
    Documentation  Local Host Acceptance Tests - Negative Scenarios
    Force Tags  Local  Acceptance  Negative

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
    Try to create a directory: no directory access permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no access to a directory can not create a subdirectory.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to create a directory via the FTP client results in an error.

        [Template]  Try to create a directory

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_group}        user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_super_group}  user=rw  group=rw  other=rw

    Try to create a directory: no directory write permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no write permission on a directory can not create a subdirectory.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to create a directory via the FTP client results in an error.

        [Template]  Try to create a directory

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rx  group=rx  other=rx
        ${dfs_super_user}  ${dfs_group}        user=rx  group=rx  other=rx
        ${dfs_super_user}  ${dfs_super_group}  user=rx  group=rx  other=rx

    Try to remove a directory: no directory access permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no access to a directory can not remove a subdirectory.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to remove a directory via the FTP client results in an error.

        [Template]  Try to remove a directory

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_group}        user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_super_group}  user=rw  group=rw  other=rw

    Try to remove a directory: no directory write permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no write permission on a directory can not remove a subdirectory.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to remove a directory via the FTP client results in an error.

        [Template]  Try to remove a directory

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rx  group=rx  other=rx
        ${dfs_super_user}  ${dfs_group}        user=rx  group=rx  other=rx
        ${dfs_super_user}  ${dfs_super_group}  user=rx  group=rx  other=rx

    Try to remove a non-empty directory
        [Tags]  Miscellaneous
        [Documentation]  Verify that attempting to remove a non-empty directory results in an error.

        # Setup
        HDFS.Create Directory  ${dfs_remote_dir}/${squeamish}
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_owner}  ${dfs_group}
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin

        # Action/Verification
        Run Keyword And Expect Error  FtpLibraryError: 550 *  FTP.Remove Directory  ${ftp_remote_dir}

    Try to remove a non-existent directory
        [Tags]  Miscellaneous
        [Documentation]  Verify that attempting to remove a non-existent directory results in an error.

        # Action/Verification
        Run Keyword And Expect Error  FtpLibraryError: 550 *  FTP.Remove Directory  ${ftp_remote_dir}/nothing-here

    Try to upload a file: no directory access permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no access to a directory can not upload a file.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to upload a file via the FTP client results in an error.

        [Template]  Try to upload a file

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_group}        user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_super_group}  user=rw  group=rw  other=rw

    Try to upload a file: no directory write permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no write permission on a directory can not upload a file.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to upload a file via the FTP client results in an error.

        [Template]  Try to upload a file

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rx  group=rx  other=rx
        ${dfs_super_user}  ${dfs_group}        user=rx  group=rx  other=rx
        ${dfs_super_user}  ${dfs_super_group}  user=rx  group=rx  other=rx

    Try to overwrite a file: no file write permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no write permission on a file can not overwrite the file.
        ...
        ...  Using the HDFS client, set the file owner/group & permissions.
        ...  Verify that attempting to overwrite a file via the FTP client results in an error.

        [Template]  Try to overwrite a file

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=r  group=r  other=r
        ${dfs_super_user}  ${dfs_group}        user=r  group=r  other=r
        ${dfs_super_user}  ${dfs_super_group}  user=r  group=r  other=r

    Try to append to a file: no file write permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no write permission on a file can not append to the file.
        ...
        ...  Using the HDFS client, set the file owner/group & permissions.
        ...  Verify that attempting to append to a file via the FTP client results in an error.

        [Template]  Try to append to a file

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=r  group=r  other=r
        ${dfs_super_user}  ${dfs_group}        user=r  group=r  other=r
        ${dfs_super_user}  ${dfs_super_group}  user=r  group=r  other=r

    Try to download a file: no directory access permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no access to a directory can not download a file.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to download a file via the FTP client results in an error.

        [Template]  Try to download a file

        # Template Setup/Action/Verification
        FROM DIRECTORY  ${dfs_owner}       ${dfs_super_group}  user=rw  group=rw  other=rw
        FROM DIRECTORY  ${dfs_super_user}  ${dfs_group}        user=rw  group=rw  other=rw
        FROM DIRECTORY  ${dfs_super_user}  ${dfs_super_group}  user=rw  group=rw  other=rw

    Try to download a file: no file read permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no read permission on a file can not download the file.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to download a file via the FTP client results in an error.

        [Template]  Try to download a file

        # Template Setup/Action/Verification
        FROM FILE  ${dfs_owner}       ${dfs_super_group}  user=wx  group=wx  other=wx
        FROM FILE  ${dfs_super_user}  ${dfs_group}        user=wx  group=wx  other=wx
        FROM FILE  ${dfs_super_user}  ${dfs_super_group}  user=wx  group=wx  other=wx

    Try to download a non-existent file
        [Tags]  Miscellaneous
        [Documentation]  Verify that attempting to download a non-existent file results in an error.

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Download File  ${ftp_remote_dir}/no-file-here  ${local_tmp_dir}/data.bin

    Try to get the modification time of a file: no directory access permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no access to a directory can not get the modification time of a file.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to get the modification time via the FTP client results in an error.

        [Template]  Try to get the modification time of a file

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_group}        user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_super_group}  user=rw  group=rw  other=rw

    Try to get the size of a file: no directory access permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no access to a directory can not get the size of a file.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to get the file size via the FTP client results in an error.

        [Template]  Try to get the size of a file

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_group}        user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_super_group}  user=rw  group=rw  other=rw

    Try to rename a file: no directory access permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no access to a directory can not rename a file.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to rename a file via the FTP client results in an error.

        [Template]  Try to rename a file

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_group}        user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_super_group}  user=rw  group=rw  other=rw

    Try to rename a file to an existing file
        [Tags]  Miscellaneous
        [Documentation]  Verify that attempting to rename a file to an existing file results in an error.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  1MB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${dfs_owner}  ${dfs_group}
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/exists.bin
        HDFS.Set Owner  ${dfs_remote_dir}/exists.bin  ${dfs_owner}  ${dfs_group}

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Rename File  ${ftp_remote_dir}/data.bin  ${ftp_remote_dir}/exists.bin

    Try to delete a file: no directory access permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no access to a directory can not delete a file.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to delete a file via the FTP client results in an error.

        [Template]  Try to delete a file

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_group}        user=rw  group=rw  other=rw
        ${dfs_super_user}  ${dfs_super_group}  user=rw  group=rw  other=rw

    Try to delete a file: no directory write permission
        [Tags]  Permissions
        [Documentation]  Verify that a user with no write permission on a directory can not delete a file.
        ...
        ...  Using the HDFS client, set the directory owner/group & permissions.
        ...  Verify that attempting to delete a file via the FTP client results in an error.

        [Template]  Try to delete a file

        # Template Setup/Action/Verification
        ${dfs_owner}       ${dfs_super_group}  user=rx  group=rx  other=rx
        ${dfs_super_user}  ${dfs_group}        user=rx  group=rx  other=rx
        ${dfs_super_user}  ${dfs_super_group}  user=rx  group=rx  other=rx

    Try to delete a non-existent file
        [Tags]  Miscellaneous
        [Documentation]  Verify that attempting to delete a non-existent file results in an error.

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Remove File  ${ftp_remote_dir}/no-file-here

    *** Keywords ***
    Try to create a directory
        [Arguments]  ${usr}  ${grp}  &{kwargs}

        # Setup
        HDFS.Set Owner  ${dfs_remote_dir}  ${usr}  ${grp}
        HDFS.Set Permissions  ${dfs_remote_dir}  &{kwargs}

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Create Directory  ${ftp_remote_dir}/${squeamish}

    Try to remove a directory
        [Arguments]  ${usr}  ${grp}  &{kwargs}

        # Setup
        HDFS.Set Owner  ${dfs_remote_dir}  ${usr}  ${grp}
        HDFS.Set Permissions  ${dfs_remote_dir}  &{kwargs}
        HDFS.Create Directory  ${dfs_remote_dir}/${squeamish}

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Remove Directory  ${ftp_remote_dir}/${squeamish}

    Try to upload a file
        [Arguments]  ${usr}  ${grp}  &{kwargs}

        # Setup
        HDFS.Set Owner  ${dfs_remote_dir}  ${usr}  ${grp}
        HDFS.Set Permissions  ${dfs_remote_dir}  &{kwargs}
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin

        #
        # NOTE: We are getting Errno 104/10054 errors from the FTP Client in Jenkins.
        # Seems to be some kind of network/firewall issue that is causing the connection to terminate?
        #
        # NOTE: Figured it out! The Harmony 5.3.0.X Server does not detect that the directory is
        # unwritable before opening the OutputStream to the HDFS Server. It then gets an exception
        # from the URI and closes the FTP data channel. It seems that in a firewall/proxy environment
        # remote connections getting closed are treated differently somehow than connections that are
        # straight to the FTP Server. Not sure if there is an elegant solution this, will need to think
        # on it a bit. For now, use the inelegant solution:
        #
        # NOTE: Workaround by closing/reopening the FTP connection inside this function so that
        # that the control channel buffer gets flushed, then also expect an [Errno ???] error in
        # addition to the normal 553 response you would expect in this situation.
        #
        Disconnect from FTP
        Connect to FTP

        # Action/Verification
        ${error} =
        ...  Run Keyword And Expect Error  *
        ...  FTP.Upload File  ${file}  ${ftp_remote_dir}/data.bin

        Should Match Regexp  ${error}  FtpLibraryError: (553 .*|\[Errno [\\d]+\] .*)

    Try to overwrite a file
        [Arguments]  ${usr}  ${grp}  &{kwargs}

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${usr}  ${grp}
        HDFS.Set Permissions  ${dfs_remote_dir}/data.bin  &{kwargs}

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 553 *
        ...  FTP.Upload File  ${file}  ${ftp_remote_dir}/data.bin

    Try to append to a file
        [Arguments]  ${usr}  ${grp}  &{kwargs}

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  1MB  data.bin
        ${data} =  TestUtils.Create Test File  ${local_tmp_dir}  2MB
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${usr}  ${grp}
        HDFS.Set Permissions  ${dfs_remote_dir}/data.bin  &{kwargs}

        # Action
        Run Keyword And Expect Error
        ...  FtpLibraryError: 553 *
        ...  FTP.Append To File  ${data}  ${ftp_remote_dir}/data.bin

    Try to download a file
        [Arguments]  ${from}  ${usr}  ${grp}  &{kwargs}

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin

        Run Keyword If  '${from}' == 'FROM FILE'
        ...  HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${usr}  ${grp}
        Run Keyword If  '${from}' == 'FROM FILE'
        ...  HDFS.Set Permissions  ${dfs_remote_dir}/data.bin  &{kwargs}
        Run Keyword If  '${from}' == 'FROM DIRECTORY'
        ...  HDFS.Set Owner  ${dfs_remote_dir}  ${usr}  ${grp}
        Run Keyword If  '${from}' == 'FROM DIRECTORY'
        ...  HDFS.Set Permissions  ${dfs_remote_dir}  &{kwargs}

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Download File  ${ftp_remote_dir}/data.bin  ${local_tmp_dir}/data.bin

    Try to get the modification time of a file
        [Arguments]  ${usr}  ${grp}  &{kwargs}

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${usr}  ${grp}
        HDFS.Set Permissions  ${dfs_remote_dir}  &{kwargs}

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 553 *
        ...  FTP.Get Modified Time  ${ftp_remote_dir}/data.bin

    Try to get the size of a file
        [Arguments]  ${usr}  ${grp}  &{kwargs}

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${usr}  ${grp}
        HDFS.Set Permissions  ${dfs_remote_dir}  &{kwargs}

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 553 *
        ...  FTP.Get File Size  ${ftp_remote_dir}/data.bin

    Try to rename a file
        [Arguments]  ${usr}  ${grp}  &{kwargs}

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/original.bin
        HDFS.Set Owner  ${dfs_remote_dir}/original.bin  ${dfs_owner}  ${dfs_group}

        HDFS.Set Owner  ${dfs_remote_dir}  ${usr}  ${grp}
        HDFS.Set Permissions  ${dfs_remote_dir}  &{kwargs}

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Rename File  ${ftp_remote_dir}/original.bin  ${ftp_remote_dir}/renamed.bin

    Try to delete a file
        [Arguments]  ${usr}  ${grp}  &{kwargs}

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${dfs_owner}  ${dfs_group}

        HDFS.Set Owner  ${dfs_remote_dir}  ${usr}  ${grp}
        HDFS.Set Permissions  ${dfs_remote_dir}  &{kwargs}

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Remove File  ${ftp_remote_dir}/data.bin
