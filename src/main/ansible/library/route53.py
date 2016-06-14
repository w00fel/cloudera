#!/usr/bin/env python

import sys

try:
    import boto
    import boto.route53
except ImportError:
    print "failed=True msg='boto required for this module'"
    sys.exit(1)

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(
        dict(
            zone=dict(required=True)
        )
    )

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    zone = module.params['zone']
    region = module.params['region']

    conn = boto.connect_route53()
    records = [r for r in conn.get_all_rrsets(zone) if r.type == "CNAME"]

    hosts = {
        'workers': []
    }

    changed = False
    for record in records:
        name = record.name
        value = record.resource_records[0]

        if name.startswith('manager'):
            hosts['manager'] = value
        elif name.startswith('master'):
            hosts['master'] = value
        elif name.startswith('primary'):
            hosts['primary'] = value
        elif name.startswith('secondary'):
            hosts['secondary'] = value
        elif name.startswith('worker'):
            hosts['workers'].append(value)

    module.exit_json(changed=changed, hosts=hosts)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

if __name__ == '__main__':
    main()
