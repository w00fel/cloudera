#!/bin/bash
#
# installers: http://contd.cleo.com/nexus/content/groups/public/com/cleo/installers/

KDC='{{kdcHost}}'
MANAGER='{{managerHost}}'
SSH_OPTIONS='-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'

wget http://${MANAGER}:7180/cmf/services/2/client-config --output-document ${HOME}/hadoop-conf.zip
unzip ${HOME}/hadoop-conf.zip -d ${HOME}/Harmony/conf

${HOME}/Harmony/Harmonyc -i ${HOME}/local-listener.xml
${HOME}/Harmony/Harmonyc -i ${HOME}/local-ftp.xml
${HOME}/Harmony/Harmonyc -i ${HOME}/cdh-ftp.xml
${HOME}/Harmony/Harmonyc -i ${HOME}/remote-ftp.xml

# Configure Kerberos
mkdir ${HOME}/Harmony/conf/kerberos
scp ${SSH_OPTIONS} ubuntu@${KDC}:hdfs.keytab ${HOME}/Harmony/conf/kerberos
scp ${SSH_OPTIONS} ubuntu@${KDC}:nobody.keytab ${HOME}/Harmony/conf/kerberos
scp ${SSH_OPTIONS} ubuntu@${KDC}:/etc/krb5.conf ${HOME}
