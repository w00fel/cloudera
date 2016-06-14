#!/bin/bash
#
# patches: http://contd.cleo.com/nexus/content/groups/public/com/cleo/patches/
# installers: http://contd.cleo.com/nexus/content/groups/public/com/cleo/installers/

# Install Harmony
aws s3 cp s3://{{bucket}}/harmony/Harmony-{{version}}-linux64-jre18.bin ${HOME}/install.bin
chmod 755 ${HOME}/install.bin

${HOME}/install.bin -i silent

# Install HDFS Connector
aws s3 cp s3://{{bucket}}/harmony/uri-hdfs-{{hdfs-version}}-import.zip ${HOME}/uri-hdfs-import.zip
chmod 644 ${HOME}/uri-hdfs-import.zip

${HOME}/Harmony/Harmonyc -i ${HOME}/uri-hdfs-import.zip
mv -f ${HOME}/Harmony/conf/system.properties.hdfs ${HOME}/Harmony/conf/system.properties
mv -f ${HOME}/Harmony/conf/vfs.yaml.hdfs ${HOME}/Harmony/conf/vfs.yaml

# Install (optional) patch
if [ "X{{patch}}" != "X" ]; then
    aws s3 cp s3://{{bucket}}/harmony/patches-{{patch}}.zip ${HOME}/patches.zip
    chmod 644 ${HOME}/patches.zip

    unzip ${HOME}/patches.zip 'Harmony/*' -d ${HOME}
    PATCH=`ls ${HOME}/Harmony/*.zip`
    ${HOME}/Harmony/Harmonyc -i `basename ${PATCH}`
fi
