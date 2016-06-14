import os
import sys
import stat

from robot.utils import asserts

class AnsibleLibrary(object):
    def __init__(self):
        pass

    def run_playbook(self, directory, playbook, remote_user='ubuntu'):
        os.environ['ANSIBLE_CONFIG'] = os.path.join(directory, 'ansible.cfg')
        rc = _run_playbook(directory, playbook, remote_user)
        asserts.assert_true(rc == 0)

def _run_playbook(directory, playbook, remote_user):
    # import late so that the os.environ[] line above gets
    # called before importing the main ansible modules.
    import ansible.playbook

    from ansible import utils
    from ansible import errors
    from ansible import callbacks
    from ansible.callbacks import display

    # add the local libraries to the global python path.
    local_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.environ['PYTHONPATH'] = local_module_path

    playbook = os.path.join(directory, playbook)
    if not os.path.exists(playbook):
        raise errors.AnsibleError("the playbook: %s could not be found" % playbook)
    if not (os.path.isfile(playbook) or stat.S_ISFIFO(os.stat(playbook).st_mode)):
        raise errors.AnsibleError("the playbook: %s does not appear to be a file" % playbook)

    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    hosts = os.path.join(directory, 'inventory', 'hosts')
    inventory = ansible.inventory.Inventory(host_list=hosts)

    pb = ansible.playbook.PlayBook(forks=1,
        playbook=playbook,
        inventory=inventory,
        remote_user=remote_user,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats
    )

    failed_hosts = []
    unreachable_hosts = []

    try:
        pb.run()

        hosts = sorted(pb.stats.processed.keys())
        display(callbacks.banner("PLAY RECAP"))
        playbook_cb.on_stats(pb.stats)

        for h in hosts:
            t = pb.stats.summarize(h)
            if t['failures'] > 0:
                failed_hosts.append(h)
            if t['unreachable'] > 0:
                unreachable_hosts.append(h)

        for h in hosts:
            t = pb.stats.summarize(h)
            display("%s : %s %s %s %s" % (
                "%-26s" % h,
                "%s=%-4s" % ('ok', str(t['ok'])),
                "%s=%-4s" % ('changed', str(t['changed'])),
                "%s=%-4s" % ('unreachable', str(t['unreachable'])),
                "%s=%-4s" % ('failed', str(t['failures'])))
            )

        if len(failed_hosts) > 0:
            return 2
        if len(unreachable_hosts) > 0:
            return 3

    except errors.AnsibleError, e:
        display(u"ERROR: %s" % utils.unicode.to_unicode(e, nonstring='simplerepr'))
        return 1

    return 0
