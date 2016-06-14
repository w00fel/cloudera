#!/bin/bash

HOSTNAME=$(/usr/bin/curl -s http://169.254.169.254/latest/meta-data/public-hostname)
sed -i "s/HOSTNAME/${HOSTNAME}/" /etc/krb5.conf

# Create the 'realm' database
kdb5_util -P hadoop create -s

service krb5-kdc restart
service krb5-admin-server restart

# Create the 'admin' user
kadmin.local -q 'addprinc -pw admin root/admin'

# Create the 'test' users
kadmin.local -q 'addprinc -pw cleo nobody'
ktutil << EOF
addent -password -p nobody@HADOOP -k 1 -e aes256-cts
cleo
wkt /home/ubuntu/nobody.keytab
quit
EOF
chown ubuntu:ubuntu /home/ubuntu/nobody.keytab

kadmin.local -q 'addprinc -pw cleo hdfs'
ktutil << EOF
addent -password -p hdfs@HADOOP -k 1 -e aes256-cts
cleo
wkt /home/ubuntu/hdfs.keytab
quit
EOF
chown ubuntu:ubuntu /home/ubuntu/hdfs.keytab
