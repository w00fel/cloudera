#!/usr/bin/env python

from __future__ import print_function

from cm_api.api_client import ApiResource

import subprocess
import boto
import time
import sys

PRIVATE_ZONE_ID = "{{privateZone}}"
LOG = open('/home/ubuntu/cloudera/bootstrap.log', 'a', 0)

# Bootstrap Cluster
print("Bootstrapping CDH Cluster", file=LOG)
args = []
args.append('/home/ubuntu/cloudera/director-client/bin/cloudera-director')
args.append('bootstrap')
args.append('/home/ubuntu/cloudera/cluster.conf')

rc = subprocess.Popen(args, stdout=LOG, stderr=subprocess.STDOUT).wait()
if rc != 0:
    sys.exit(rc);

print("Geting CDH Manager DNS Record", file=LOG)
conn = boto.connect_route53()

records = [r for r in conn.get_all_rrsets(PRIVATE_ZONE_ID) if r.type == "CNAME"]
for record in records:
    if record.name.startswith('manager'):
        MANAGER = record.name
        break;

#
# Give the cluster time to startup and stabilize...
#
# TODO, it would be better to wake up every minute or so and check if the
# cluster is ready for action.
#
time.sleep(120)

print("Kerberizing CDH Cluster", file=LOG)
args = []
args.append('/home/ubuntu/cloudera/kerberize.py')
args.append(MANAGER)
args.append('CDH-Cluster-AWS')

rc = subprocess.Popen(args, stdout=LOG, stderr=subprocess.STDOUT).wait()
if rc != 0:
    sys.exit(rc);

print("Enabling HDFS Name Node HA", file=LOG)
args = []
args.append('/home/ubuntu/cloudera/enable-hdfs-ha.py')
args.append('--host')
args.append(MANAGER)
args.append('CDH-Cluster-AWS')
args.append('CDH-Cluster-NameService')

sys.exit(subprocess.Popen(args, stdout=LOG, stderr=subprocess.STDOUT).wait())
