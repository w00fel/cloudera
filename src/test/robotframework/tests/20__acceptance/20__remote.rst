Remote Host Acceptance Tests
----------------------------

The remote host acceptance tests use an FTP client on the Harmony server to connect to a 'remote'
host configured to use HDFS for its inbox/outbox. The 'remote' host is actually on the same server
to make deployment easier, and the connection is done via loopback.

The SOAP client is used to trigger one of the following pre-configured actions::

    <append> PUT -DEL -APE * inbox/
    <receive> GET outbox/*
    <send> PUT -DEL * inbox/

There is one test for each action.

.. code:: robotframework

    *** Settings ***
    Documentation  Remote Host Acceptance Tests
    Force Tags  Remote  Acceptance  Positive

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
    ${host}  Remote FTP Hosts
    ${mailbox}  loopback

    *** Keywords ***
    Setup for suite
        [Documentation]  Create suite level inbox/outbox variables.

        Set Suite Variable  ${local_inbox}  ${ssh_path}/inbox/${mailbox}
        Set Suite Variable  ${local_outbox}  ${ssh_path}/outbox/${mailbox}
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
