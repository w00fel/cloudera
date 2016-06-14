LCOPY Acceptance Tests
----------------------

The LCOPY acceptance tests use the LCOPY command on the Harmony server to move files between a
local user inbox/outbox to/from an HDFS user inbox/outbox

The SOAP client is used to trigger one of the following pre-configured actions::

    <append> LCOPY -DEL -APE %outbox%/* "vfs:/templates=hadoop/remote/inbox/" 
    <receive> LCOPY "vfs:/templates=hadoop/remote/outbox/*" %inbox%
    <send> LCOPY -DEL %outbox%/* "vfs:/templates=hadoop/remote/inbox/"

There is one test for each action.

.. code:: robotframework

    *** Settings ***
    Documentation  LCOPY Acceptance Tests
    Force Tags  LCOPY  Acceptance  Positive

    Resource  ${test.dir}/common.rst
    Resource  actions.rst

    Suite Setup  Run Keywords
    ...  Connect to HDFS  ${dfs_login}  remote  AND
    ...  Connect to SSH  AND
    ...  Setup for suite

    Suite Teardown  Run Keywords
    ...  Disconnect from HDFS  AND
    ...  Disconnect from SSH

    Test Setup  Setup for tests
    Test Teardown  Cleanup after tests

    *** Variables ***
    ${host}  Local FTP Users
    ${mailbox}  local

    *** Keywords ***
    Setup for suite
        [Documentation]  Create suite level inbox/outbox variables.

        Set Suite Variable  ${local_inbox}  ${ssh_path}/local/root/${mailbox}/inbox
        Set Suite Variable  ${local_outbox}  ${ssh_path}/local/root/${mailbox}/outbox
        Set Suite Variable  ${remote_inbox}  ${dfs_root_dir}/inbox
        Set Suite Variable  ${remote_outbox}  ${dfs_root_dir}/outbox

    *** Test Cases ***
    Run action to send files from local outbox to remote inbox
        [Documentation]  Run the '${host}/${mailbox}/<send>' action.
        [Template]  Run send action

        # Template Setup/Action/Verification
        ${host}  ${mailbox}

    Run action to append files from local outbox to remote inbox
        [Documentation]  Run the '${host}/${mailbox}/<append>' action.
        [Template]  Run append action

        # Template Setup/Action/Verification
        ${host}  ${mailbox}

    Run action to receive files from remote outbox to local inbox
        [Documentation]  Run the '${host}/${mailbox}/<receive>' action.
        [Template]  Run receive action

        # Template Setup/Action/Verification
        ${host}  ${mailbox}
