Provision AWS Kerberos/CDH Cluster/Harmony Server
-------------------------------------------------

.. code:: robotframework

    *** Settings ***
    Documentation  Provision AWS Kerberos/CDH Cluster/Harmony Server
    Force Tags  Environment

    Library  Libraries/AnsibleLibrary.py

    *** Test Cases ***
    Provision test environment
        [Documentation]  Provison the AWS test environment.

        ${enabled} =  Evaluate  '${provision}'.lower() in ['1', 'true', 'y', 'yes', 'yup', 'on']

        Run Keyword If      ${enabled}  Run Playbook    ${ansible.dir}  provision.yaml
        Run Keyword Unless  ${enabled}  Pass Execution  Skipping provisioning  Skipped
