.. code:: robotframework

    *** Keywords ***
    Run send action
        [Documentation]  Run a preconfigured <send> action.
        ...
        ...  Setup:
        ...     - Upload files to local outbox via SSH client
        ...  Action:
        ...     - Run <send> action: transfers files from local outbox -> remote inbox
        ...  Verification:
        ...     - Compare checksums of uploaded files with those on the HDFS file system
        [Arguments]  ${host}  ${mailbox}

        # Setup
        SSH.Upload File  ${data.dir}/${bacon}  ${local_outbox}/${timestamp}-${bacon}
        SSH.Upload File  ${data.dir}/${eggs}  ${local_outbox}/${timestamp}-${eggs}
        SSH.Upload File  ${data.dir}/${spam}  ${local_outbox}/${timestamp}-${spam}

        # Action
        Host Action.Run  ${host}  ${mailbox}  send

        # Verification
        Verify Checksums Match  ${data.dir}/${bacon}  ${remote_inbox}/${timestamp}-${bacon}
        Verify Checksums Match  ${data.dir}/${eggs}  ${remote_inbox}/${timestamp}-${eggs}
        Verify Checksums Match  ${data.dir}/${spam}  ${remote_inbox}/${timestamp}-${spam}

        # Cleanup
        HDFS.Remove File  ${remote_inbox}/${timestamp}-${bacon}
        HDFS.Remove File  ${remote_inbox}/${timestamp}-${eggs}
        HDFS.Remove File  ${remote_inbox}/${timestamp}-${spam}

    Run append action
        [Documentation]  Run a preconfigured <append> action.
        ...
        ...  Setup:
        ...     - Upload files to local outbox via SSH client
        ...     - Upload files to remote inbox via HDFS client
        ...  Action:
        ...     - Run <append> action: appends files from local outbox -> remote inbox
        ...  Verification:
        ...     - Compare checksums of appended files with those on the HDFS file system
        [Arguments]  ${host}  ${mailbox}

        # Setup
        SSH.Upload File  ${data.dir}/${bacon}  ${local_outbox}/${timestamp}-${bacon}
        SSH.Upload File  ${data.dir}/${eggs}  ${local_outbox}/${timestamp}-${eggs}
        SSH.Upload File  ${data.dir}/${spam}  ${local_outbox}/${timestamp}-${spam}

        HDFS.Upload File  ${data.dir}/${bacon}  ${remote_inbox}/${timestamp}-${bacon}
        HDFS.Upload File  ${data.dir}/${eggs}  ${remote_inbox}/${timestamp}-${eggs}
        HDFS.Upload File  ${data.dir}/${spam}  ${remote_inbox}/${timestamp}-${spam}

        # Action
        Host Action.Run  ${host}  ${mailbox}  append

        # Verification
        ${appended_bacon} =  Append Test Files  ${local_tmp_dir}  ${data.dir}/${bacon}
        ${appended_eggs} =  Append Test Files  ${local_tmp_dir}  ${data.dir}/${eggs}
        ${appended_spam} =  Append Test Files  ${local_tmp_dir}  ${data.dir}/${spam}

        Verify Checksums Match  ${appended_bacon}  ${remote_inbox}/${timestamp}-${bacon}
        Verify Checksums Match  ${appended_eggs}  ${remote_inbox}/${timestamp}-${eggs}
        Verify Checksums Match  ${appended_spam}  ${remote_inbox}/${timestamp}-${spam}

        # Cleanup
        HDFS.Remove File  ${remote_inbox}/${timestamp}-${bacon}
        HDFS.Remove File  ${remote_inbox}/${timestamp}-${eggs}
        HDFS.Remove File  ${remote_inbox}/${timestamp}-${spam}

    Run receive action
        [Documentation]  Run a preconfigured <receive> action.
        ...
        ...  Setup:
        ...     - Upload files to remote outbox via HDFS client
        ...  Action:
        ...     - Run <receive> action: transfers files from remote outbox -> local inbox
        ...  Verification:
        ...     - Retrieve files in local inbox via SSH client
        ...     - Compare checksums of retrieved files with those on the HDFS file system
        [Arguments]  ${host}  ${mailbox}

        # Setup
        HDFS.Upload File  ${data.dir}/${bacon}  ${remote_outbox}/${timestamp}-${bacon}
        HDFS.Upload File  ${data.dir}/${eggs}  ${remote_outbox}/${timestamp}-${eggs}
        HDFS.Upload File  ${data.dir}/${spam}  ${remote_outbox}/${timestamp}-${spam}

        # Action
        Host Action.Run  ${host}  ${mailbox}  receive

        # Verification
        SSH.Download File  ${local_inbox}/${timestamp}-${bacon}  ${local_tmp_dir}/${bacon}
        SSH.Download File  ${local_inbox}/${timestamp}-${eggs}  ${local_tmp_dir}/${eggs}
        SSH.Download File  ${local_inbox}/${timestamp}-${spam}  ${local_tmp_dir}/${spam}

        Verify Checksums Match  ${local_tmp_dir}/${bacon}  ${remote_outbox}/${timestamp}-${bacon}
        Verify Checksums Match  ${local_tmp_dir}/${eggs}  ${remote_outbox}/${timestamp}-${eggs}
        Verify Checksums Match  ${local_tmp_dir}/${spam}  ${remote_outbox}/${timestamp}-${spam}

        # Cleanup
        SSH.Remove File  ${local_inbox}/${timestamp}-${bacon}
        SSH.Remove File  ${local_inbox}/${timestamp}-${eggs}
        SSH.Remove File  ${local_inbox}/${timestamp}-${spam}

        HDFS.Remove File  ${remote_outbox}/${timestamp}-${bacon}
        HDFS.Remove File  ${remote_outbox}/${timestamp}-${eggs}
        HDFS.Remove File  ${remote_outbox}/${timestamp}-${spam}
