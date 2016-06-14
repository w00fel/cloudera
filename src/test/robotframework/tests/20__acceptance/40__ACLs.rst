HDFS ACLs Acceptance Tests
--------------------------

The Local Host Acceptance Tests have already tested that the POSIX permissions are being honored, these
tests are concerned with verifying that the POSIX permissions can be relaxed or restricted via ACLs.

Two basic scenarios are tested:

* Verifying that restrictive POSIX permissions can be relaxed
* Verifying that permissive POSIX permissions can be restricted

.. code:: robotframework

    *** Settings ***
    Documentation  HDFS ACLs Acceptance Tests
    Force Tags  Acceptance  ACLs

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
    Relax POSIX directory permissions on upload
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxr-x
        ...  and verify that an upload to that directory fails.
        ...  Then set the ACL to allow write for the user nobody, upload the file again
        ...  and verify that the transfer is now succesful.

        # Setup
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rx

        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin

        # Action/Verification
        Upload and expect error  ${file}

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rwx
        FTP.Upload File  ${file}  ${ftp_remote_dir}/data.bin

    Restrict POSIX directory permissions on upload
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxrwx
        ...  and verify that an upload to that directory is successful.
        ...  Then set the ACL to disallow write for the user nobody, upload the file again
        ...  and verify that the transfer now fails.

        # Setup
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rwx

        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin

        # Action/Verification
        FTP.Upload File  ${file}  ${ftp_remote_dir}/data.bin

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:r-x
        Upload and expect error  ${file}

    Relax POSIX file permissions on overwrite
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a file owned by hdfs/supergroup to rw-rw-r--
        ...  and verify that an attempt to overwrite that file fails.
        ...  Then set the ACL to allow write for the user nobody, upload the file again
        ...  and verify that the transfer is now succesful.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin

        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}/data.bin  user=rw  group=rw  other=r

        # Action/Verification
        Upload and expect error  ${file}

        HDFS.Set Acl  ${dfs_remote_dir}/data.bin  user:nobody:rw-
        FTP.Upload File  ${file}  ${ftp_remote_dir}/data.bin

    Restrict POSIX file permissions on overwrite
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a file owned by hdfs/supergroup to rw-rw-rw-
        ...  and verify that an attempt to overwrite that file is successful.
        ...  Then set the ACL to disallow write for the user nobody, upload the file again
        ...  and verify that the transfer now fails.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin

        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}/data.bin  user=rw  group=rw  other=rw

        # Action/Verification
        FTP.Upload File  ${file}  ${ftp_remote_dir}/data.bin

        # NOTE: Successful upload changes file owner to 'nobody' so we need to reset it back to 'hdfs'
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Acl  ${dfs_remote_dir}/data.bin  user:nobody:r--
        Upload and expect error  ${file}

    Relax POSIX file permissions on append
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a file owned by hdfs/supergroup to rw-rw-r--
        ...  and verify that an attempt to append to that file fails.
        ...  Then set the ACL to allow write for the user nobody, upload the file again
        ...  and verify that the transfer is now succesful.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin

        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}/data.bin  user=rw  group=rw  other=r

        # Action/Verification
        Upload and expect error  ${file}

        HDFS.Set Acl  ${dfs_remote_dir}/data.bin  user:nobody:rw-
        FTP.Append To File  ${file}  ${ftp_remote_dir}/data.bin

    Restrict POSIX file permissions on append
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a file owned by hdfs/supergroup to rw-rw-rw-
        ...  and verify that an attempt to append to that file is successful.
        ...  Then set the ACL to disallow write for the user nobody, upload the file again
        ...  and verify that the transfer now fails.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin

        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}/data.bin  user=rw  group=rw  other=rw

        # Action/Verification
        FTP.Append To File  ${file}  ${ftp_remote_dir}/data.bin

        # NOTE: Successful append changes file owner to 'nobody' so we need to reset it back to 'hdfs'
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Acl  ${dfs_remote_dir}/data.bin  user:nobody:r--
        Upload and expect error  ${file}

    Relax POSIX directory permissions on download
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwx-w-
        ...  and verify that an attempt to download that file fails.
        ...  Then set the ACL to allow read for the user nobody, download the file again
        ...  and verify that the transfer is now successful.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=w

        # Action/Verification
        Download and expect error

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rwx
        FTP.Download File  ${ftp_remote_dir}/data.bin  ${local_tmp_dir}/data.bin

    Restrict POSIX directory permissions on download
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a file owned by hdfs/supergroup to rwxrwxrwx
        ...  and verify that an attempt to download that file is successful.
        ...  Then set the ACL to disallow read for the user nobody, download the file again
        ...  and verify that the transfer now fails.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rwx

        # Action/Verification
        FTP.Download File  ${ftp_remote_dir}/data.bin  ${local_tmp_dir}/data.bin

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:-w-
        Download and expect error

    Relax POSIX file permissions on download
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a file owned by hdfs/supergroup to -w--w--w-
        ...  and verify that an attempt to download that file fails.
        ...  Then set the ACL to allow read for the user nobody, download the file again
        ...  and verify that the transfer is now successful.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}/data.bin  user=w  group=w  other=w

        # Action/Verification
        Download and expect error

        HDFS.Set Acl  ${dfs_remote_dir}/data.bin  user:nobody:rw-
        FTP.Download File  ${ftp_remote_dir}/data.bin  ${local_tmp_dir}/data.bin

    Restrict POSIX file permissions on download
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a file owned by hdfs/supergroup to rw-rw-rw-
        ...  and verify that an attempt to download that file is successful.
        ...  Then set the ACL to disallow read for the user nobody, download the file again
        ...  and verify that the transfer now fails.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}/data.bin  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}/data.bin  user=rw  group=rw  other=rw

        # Action/Verification
        FTP.Download File  ${ftp_remote_dir}/data.bin  ${local_tmp_dir}/data.bin

        HDFS.Set Acl  ${dfs_remote_dir}/data.bin  user:nobody:-w-
        Download and expect error

    Relax POSIX file permissions on make directory
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxr-x
        ...  and verify that an attempt to create a sub-directory fails.
        ...  Then set the ACL to allow write for the user nobody, create the sub-directory again
        ...  and verify that the command is now successful.

        # Setup
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rx

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Create Directory  ${ftp_remote_dir}/${squeamish}

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rwx
        FTP.Create Directory  ${ftp_remote_dir}/${squeamish}

    Restrict POSIX file permissions on make directory
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxrwx
        ...  and verify that an attempt to create a sub-directory is successful.
        ...  Then set the ACL to disallow write for the user nobody, create the sub-directory again
        ...  and verify that the command now fails.

        # Setup
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rwx

        # Action/Verification
        FTP.Create Directory  ${ftp_remote_dir}/${squeamish}

        FTP.Remove Directory  ${ftp_remote_dir}/${squeamish}
        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:r-x
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Create Directory  ${ftp_remote_dir}/${squeamish}

    Relax POSIX file permissions on remove directory
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxr-x
        ...  and verify that an attempt to delete the directory fails.
        ...  Then set the ACL to allow write for the user nobody, delete the directory again
        ...  and verify that the command is now successful.

        # Setup
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rx
        HDFS.Create Directory  ${dfs_remote_dir}/${squeamish}

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Remove Directory  ${ftp_remote_dir}/${squeamish}

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rwx
        FTP.Remove Directory  ${ftp_remote_dir}/${squeamish}

    Restrict POSIX file permissions on remove directory
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxrwx
        ...  and verify that an attempt to delete the directory is successful.
        ...  Then set the ACL to disallow write for the user nobody, delete the directory again
        ...  and verify that the command now fails.

        # Setup
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rwx
        HDFS.Create Directory  ${dfs_remote_dir}/${squeamish}

        # Action/Verification
        FTP.Remove Directory  ${ftp_remote_dir}/${squeamish}

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:r-x
        HDFS.Create Directory  ${dfs_remote_dir}/${squeamish}
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Remove Directory  ${ftp_remote_dir}/${squeamish}

    Relax POSIX file permissions on delete file
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxr-x
        ...  and verify that an attempt to delete a file fails.
        ...  Then set the ACL to allow write for the user nobody, delete the file again
        ...  and verify that the command is now successful.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rx

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Remove File  ${ftp_remote_dir}/data.bin

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rwx
        FTP.Remove File  ${ftp_remote_dir}/data.bin

    Restrict POSIX file permissions on delete file
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxrwx
        ...  and verify that an attempt to delete a file is successful.
        ...  Then set the ACL to disallow write for the user nobody, delete the file again
        ...  and verify that the command now fails.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rwx

        # Action/Verification
        FTP.Remove File  ${ftp_remote_dir}/data.bin

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:r-x
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Remove File  ${ftp_remote_dir}/data.bin

    Relax POSIX file permissions on file modification time
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxrw-
        ...  and verify that an attempt to get the file modification time fails.
        ...  Then set the ACL to allow access for the user nobody, get the file modification time again
        ...  and verify that the command is now successful.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rw

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 553 *
        ...  FTP.Get Modified Time  ${ftp_remote_dir}/data.bin

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rwx
        FTP.Get Modified Time  ${ftp_remote_dir}/data.bin

    Restrict POSIX file permissions on file modification time
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a file owned by hdfs/supergroup to rwxrwxrwx
        ...  and verify that an attempt to get the file modification time is successful.
        ...  Then set the ACL to disallow access for the user nobody, get the file modification time again
        ...  and verify that the command now fails.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rwx

        # Action/Verification
        FTP.Get Modified Time  ${ftp_remote_dir}/data.bin

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rw-
        Run Keyword And Expect Error
        ...  FtpLibraryError: 553 *
        ...  FTP.Get Modified Time  ${ftp_remote_dir}/data.bin

    Relax POSIX file permissions on file size
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxrw-
        ...  and verify that an attempt to get the file size fails.
        ...  Then set the ACL to allow access for the user nobody, get the file size again
        ...  and verify that the command is now successful.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rw

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 553 *
        ...  FTP.Get File Size  ${ftp_remote_dir}/data.bin

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rwx
        FTP.Get FIle Size  ${ftp_remote_dir}/data.bin

    Restrict POSIX file permissions on file size
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a file owned by hdfs/supergroup to rwxrwxrwx
        ...  and verify that an attempt to get the file size is successful.
        ...  Then set the ACL to disallow access for the user nobody, get the file size again
        ...  and verify that the command now fails.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/data.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rwx

        # Action/Verification
        FTP.Get File Size  ${ftp_remote_dir}/data.bin

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rw-
        Run Keyword And Expect Error
        ...  FtpLibraryError: 553 *
        ...  FTP.Get File Size  ${ftp_remote_dir}/data.bin

    Relax POSIX file permissions on file rename
        [Tags]  Positive
        [Documentation]  Verify that restrictive POSIX permissions can be relaxed.
        ...
        ...  Set the POSIX permissions of a directory owned by hdfs/supergroup to rwxrwxrw-
        ...  and verify that an attempt to rename the file fails.
        ...  Then set the ACL to allow access for the user nobody, rename the file again
        ...  and verify that the command is now successful.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/original.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rw

        # Action/Verification
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Rename File  ${ftp_remote_dir}/original.bin  ${ftp_remote_dir}/renamed.bin

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rwx
        FTP.Rename File  ${ftp_remote_dir}/original.bin  ${ftp_remote_dir}/renamed.bin

    Restrict POSIX file permissions on file rename
        [Tags]  Negative
        [Documentation]  Verify that permissive POSIX permissions can be restricted.
        ...
        ...  Set the POSIX permissions of a file owned by hdfs/supergroup to rwxrwxrwx
        ...  and verify that an attempt to rename the file is successful.
        ...  Then set the ACL to disallow access for the user nobody, rename the file again
        ...  and verify that the command now fails.

        # Setup
        ${file} =  TestUtils.Create Test File  ${local_tmp_dir}  100KB  data.bin
        HDFS.Upload File  ${file}  ${dfs_remote_dir}/original.bin
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_super_user}  ${dfs_super_group}
        HDFS.Set Permissions  ${dfs_remote_dir}  user=rwx  group=rwx  other=rwx

        # Action/Verification
        FTP.Rename File  ${ftp_remote_dir}/original.bin  ${ftp_remote_dir}/renamed.bin

        HDFS.Set Acl  ${dfs_remote_dir}  user:nobody:rw-
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Rename File  ${ftp_remote_dir}/renamed.bin  ${ftp_remote_dir}/original.bin

    *** Keywords ***
    Upload and expect error
        [Documentation]  Upload a file and expect an error.
        [Arguments]  ${file}

        # See NOTE in 10__local/20__negative.rst for details on the Errno issue.
        ${error} =
        ...  Run Keyword And Expect Error  *
        ...  FTP.Upload File  ${file}  ${ftp_remote_dir}/data.bin

        Should Match Regexp  ${error}  FtpLibraryError: (553 .*|\[Errno [\\d]+\] .*)

        Disconnect from FTP
        Connect to FTP

    Download and expect error
        [Documentation]  Download a file and expect an error.
        Run Keyword And Expect Error
        ...  FtpLibraryError: 550 *
        ...  FTP.Download File  ${ftp_remote_dir}/data.bin  ${local_tmp_dir}/data.bin
