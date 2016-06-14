from cm_api.api_client import ApiResource
import time

def hdfs_failover(manager):
    hdfs = _get_hdfs_service(_get_connection(manager))
    (active, standby) = _get_name_nodes(hdfs)

    hdfs.failover_hdfs(active.name, standby.name)
    while True:
        (new_active, new_standby) = _get_name_nodes(hdfs)
        if (new_active.name != standby.name):
            time.sleep(5)
        else:
            break;

def get_name_node_roles(manager):
    hdfs = _get_hdfs_service(_get_connection(manager))
    return _get_name_nodes(hdfs)

def get_active_name_node(manager):
    api = _get_connection(manager)
    hdfs = _get_hdfs_service(api)
    (active, standby) = _get_name_nodes(hdfs)
    return api.get_host(active.hostRef.hostId).hostname

def _get_connection(manager):
    return ApiResource(manager)

def _get_hdfs_service(api):
    cluster = api.get_cluster('CDH-Cluster-AWS')
    for service in cluster.get_all_services():
      if service.type == 'HDFS':
        return service

def _get_name_nodes(hdfs):
    active = None
    standby = None
    for role in hdfs.get_all_roles():
        if role.type == 'NAMENODE':
            if role.haStatus == 'ACTIVE':
                active = role
            else:
                standby = role
    return (active, standby)
