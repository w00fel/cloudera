#!/bin/bash

# Install AWS tools if not present
if [ ! -f /usr/local/bin/aws ]; then
    wget -nv https://s3.amazonaws.com/aws-cli/awscli-bundle.zip
    unzip awscli-bundle.zip
    awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
    rm -rf awscli-bundle*
fi

IPV4=$(/usr/bin/curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
HOSTNAME=$(/usr/bin/curl -s http://169.254.169.254/latest/meta-data/public-hostname)
INSTANCE_ID=$(/usr/bin/curl -s http://169.254.169.254/latest/meta-data/instance-id)
GROUP=$(/usr/local/bin/aws ec2 describe-tags --o text --region "{{region}}" --filters\
  "Name=resource-type,Values=instance"\
  "Name=resource-id,Values=${INSTANCE_ID}"\
  "Name=key,Values=group" | awk '{ print $5 }')

hostname "${HOSTNAME}"
if [ -f /etc/sysconfig/network ]; then
    sed -i "s/HOSTNAME.*/HOSTNAME=${HOSTNAME}/g" /etc/sysconfig/network
else
    echo "${HOSTNAME}" > /etc/hostname
fi

# Create our 'fake' private name
FAKE_DOMAIN="aws.cleo.net"
FAKE_HOST="${GROUP}-${INSTANCE_ID}-{{region}}"
FAKE_FQDN="${FAKE_HOST}.${FAKE_DOMAIN}"

cat<<JSON > /tmp/aws-r53-private.json
{
    "Changes": [{
        "Action": "UPSERT",
        "ResourceRecordSet": {
            "Name": "${FAKE_FQDN}.",
            "Type": "CNAME",
            "TTL":  300,
            "ResourceRecords": [{
                "Value": "${HOSTNAME}"
            }]
        }
    }]
}
JSON

# Get the last octet of the local IP address
OCTET=$(echo "${IPV4}" | sed -r "s/^([0-9]{1,3}\.){1,3}([0-9]{1,3})$/\2/")

cat<<JSON > /tmp/aws-r53-reverse.json
{
    "Changes": [{
        "Action": "UPSERT",
        "ResourceRecordSet": {
            "Name": "${OCTET}.0.0.10.in-addr.arpa",
            "Type": "PTR",
            "TTL":  300,
            "ResourceRecords": [{
                "Value": "${HOSTNAME}"
            }]
        }
    }]
}
JSON

# Update Route53 Private/Reverse zones

COMMAND="/usr/local/bin/aws route53 change-resource-record-sets --hosted-zone-id {{privateZone}}\
  --change-batch file:///tmp/aws-r53-private.json"
for i in {1..5}; do
   ${COMMAND} && break || sleep $((i*i))
done

COMMAND="/usr/local/bin/aws route53 change-resource-record-sets --hosted-zone-id {{reverseZone}}\
  --change-batch file:///tmp/aws-r53-reverse.json"
for i in {1..5}; do
   ${COMMAND} && break || sleep $((i*i))
done

rm -f /tmp/aws-r53-*.json
