import jmespath
from py_linq import Enumerable
import re


class KindFilter:
    def __init__(self, kind: str):
        self._kind = kind
        self._path = jmespath.compile("kind")

    def name(self, name: str):
        name_path = jmespath.compile("metadata.name")

        def match(x: Enumerable) -> bool:
            if self._path.search(x) != self._kind:
                return False

            if name_path.search(x) != name:
                return False

            return True

        return match

    def name_match(self, pattern: str):
        name_path = jmespath.compile("metadata.name")
        name_re = re.compile(pattern)

        def match(x: Enumerable) -> bool:
            if self._path.search(x) != self._kind:
                return False

            result = name_path.search(x)
            if result is None:
                return False

            return name_re.search(result) is not None

        return match


class KubeKindFilter:
    service = KindFilter("Service")
    deployment = KindFilter("Deployment")
    stateful_set = KindFilter("StatefulSet")
    daemon_set = KindFilter("DaemonSet")
    job = KindFilter("Job")
    cron_job = KindFilter("CronJob")
    pod = KindFilter("Pod")
    persistent_volume_claim = KindFilter("PersistentVolumeClaim")
    persistent_volume = KindFilter("PersistentVolume")
    secret = KindFilter("Secret")
    config_map = KindFilter("ConfigMap")
    ingress = KindFilter("Ingress")
    service_account = KindFilter("ServiceAccount")
    role = KindFilter("Role")
    role_binding = KindFilter("RoleBinding")
    cluster_role = KindFilter("ClusterRole")
    cluster_role_binding = KindFilter("ClusterRoleBinding")
    custom_resource_definition = KindFilter("CustomResourceDefinition")
