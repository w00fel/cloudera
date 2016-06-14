Teardown AWS Kerberos/CDH Cluster/Harmony Server
-------------------------------------------------

.. code:: robotframework

    *** Settings ***
    Documentation  Teardown AWS Kerberos/CDH Cluster/Harmony Server
    Force Tags  Environment

    Library  Libraries/AnsibleLibrary.py

    *** Test Cases ***
    Teardown test environment
        [Documentation]  Teardown the AWS test environment.

        ${enabled} =  Evaluate  '${teardown}'.lower() in ['1', 'true', 'y', 'yes', 'yup', 'on']

        Run Keyword If      ${enabled}  Run Playbook    ${ansible.dir}  teardown.yaml
        Run Keyword Unless  ${enabled}  Pass Execution  Skipping teardown  Skipped
