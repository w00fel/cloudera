.. code:: robotframework

    *** Settings ***

    # Robot Framework Libraries
    Library  String
    Library  Collections
    Library  OperatingSystem  WITH NAME  OS

    # Custom Libraries
    Library  TestUtils
    Library  SudsLibrary
    Library  SSHLibrary  WITH NAME  SSH
    Library  Libraries/FtpLibrary.py  WITH NAME  FTP
    Library  Libraries/HdfsLibrary.py  WITH NAME  HDFS
    Library  Libraries/ClouderaLibrary.py  WITH NAME  CDH

    # Test Config
    Variables  ${variable.file}

    *** Variables ***
    ${password}  cleo

    ${ftp_server}  ${config.harmony.server}
    ${ftp_port}  10021
    ${ftp_user}  alice
    ${ftp_password}  ${password}
    ${ftp_login}  ${ftp_user}

    ${dfs_port}  50070
    ${dfs_super_user}  hdfs
    ${dfs_super_group}  supergroup
    ${dfs_owner}  nobody
    ${dfs_group}  nobody
    ${dfs_login}  ${dfs_owner}
    ${dfs_password}  ${password}
    ${dfs_mailbox}  ${ftp_user}

    ${kerberos}  ${config.kerberos.server}

    ${ssh_server}  ${config.harmony.server}
    ${ssh_port}  22
    ${ssh_login}  ubuntu
    ${ssh_key}  ${config.ssh.key}
    ${ssh_path}  /home/${ssh_login}/Harmony

    ${soap_endpoint}  http://${config.harmony.server}:5080/services
    ${soap_password}  bubbles

    ${bacon}  bacon.txt
    ${eggs}  eggs.txt
    ${spam}  spam.txt
    ${sausage}  sausage.txt
    ${squeamish}  ossifrage

    *** Keywords ***
    Connect to HDFS
        [Documentation]  Connect to the HDFS server.
        [Arguments]  ${login}  ${mailbox}

        ${dfs_server} =  CDH.Get Active Name Node  ${config.cluster.manager}
        HDFS.Connect  ${dfs_server}  ${dfs_port}  ${kerberos}  ${login}  ${password}  root=/user/${mailbox}

        ${current_time} =  TestUtils.Get Timestamp
        Set Suite Variable  ${timestamp}  ${current_time}
        Set Suite Variable  ${ftp_remote_dir}  /${timestamp}
        Set Suite Variable  ${dfs_root_dir}  /user/${mailbox}
        Set Suite Variable  ${dfs_remote_dir}  ${dfs_root_dir}/${timestamp}

    Disconnect from HDFS
        [Documentation]  Close the HDFS server session.

        HDFS.Close

    Connect to FTP
        [Documentation]  Connect to the FTP server.
        ...
        ...  Set FTP transfer mode to image (I).

        FTP.Connect  ${ftp_server}  ${ftp_port}  ${ftp_user}  ${ftp_password}
        FTP.Send Command  TYPE I

    Disconnect from FTP
        [Documentation]  Close the FTP server session.

        FTP.Close

    Connect to SSH
        [Documentation]  Connect to the SSH server.

        SSH.Connect  ${ssh_server}  ${ssh_port}  ${ssh_login}  ${ssh_key}

    Disconnect from SSH
        [Documentation]  Close the SSH server session.
        SSH.Close Connection

    Setup for tests
        [Documentation]  Initialize test case runtime environment.
        ...
        ...  Create new local temp directory for every test case.
        ...  Create new remote working directory for every test case.

        ${tmp_dir} =  Create Temp Directory
        Set Suite Variable  ${local_tmp_dir}  ${tmp_dir}

        HDFS.Create Directory  ${dfs_remote_dir}
        HDFS.Set Owner  ${dfs_remote_dir}  ${dfs_owner}  ${dfs_group}

    Cleanup after tests
        [Documentation]  Cleanup test case runtime environment.
        ...
        ...  Delete local temp directory at the end of every test case.
        ...  Delete remote working directory at the end of every test case.

        OS.Remove Directory  ${local_tmp_dir}  recursive=yes
        HDFS.Remove Directory  ${dfs_remote_dir}


    Verify Checksums Match
        [Documentation]  Compare HDFS checksums - Fails the test if they don't match.
        ...
        ...  The HDFS file system maintains a checksum on all files that it is storing.
        ...  Retrieve this checksum and the algorithm used to compute it. Compute the
        ...  checksum on the local file using the same algorithm.
        [Arguments]  ${local_path}  ${remote_path}

        &{remote} =  HDFS.Get Checksum  ${remote_path}
        ${local_checksum} =  TestUtils.Get Checksum  ${local_path}  ${remote.algorithm}
        Should Be Equal  ${local_checksum}  ${remote.checksum}

    SSH.Connect
        [Documentation]  Connect to the SSH server.
        [Arguments]  ${server}  ${port}  ${login}  ${key}

        Open Connection  ${server}  -port=${port}
        ${output} =  SSH.Login With Public Key  ${login}  ${key}
        ${message} =  String.Get Line  ${output}  0
        [Return]  ${message}

    SSH.Upload File
        [Documentation]  Upload a file to the SSH server.
        [Arguments]  ${local_path}  ${remote_path}

        Put File  ${local_path}  ${remote_path}

    SSH.Download File
        [Documentation]  Download a file from the SSH server.
        [Arguments]  ${remote_path}  ${local_path}

        SSH.Get File  ${remote_path}  ${local_path}

    SSH.Get File Size
        [Documentation]  Send the 'get file size' command to the SSH server.
        [Arguments]  ${path}

        ${size} =  SSH.Execute Command  stat --format=%s ${path}
        [Return]  ${size}

    SSH.Remove File
        [Documentation]  Send the 'remove file' command to the SSH server.
        [Arguments]  ${path}

        SSH.Execute Command  rm -f ${path}

    SSH.Remove Directory
        [Documentation]  Send the 'remove directory' command to the SSH server.
        [Arguments]  ${path}

        SSH.Execute Command  rm -rf ${path}

    SSH.Close
        [Documentation]  Close the connection to the SSH server.

        SSH.Close Connection

    Host Action.Run
        [Documentation]  Run a Versalex Action.
        [Arguments]  ${host}  ${mailbox}  ${action}

        Create Soap Client  ${soap_endpoint}/versalexws?wsdl
        @{array} =  Create List  ${host}  ${mailbox}  ${action}
        ${result} =  Call Soap Method  run  ${soap_password}  ${array}

