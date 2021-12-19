from dataclasses import dataclass, field
import tempfile
from typing import Dict, Any
import yaml
from delegator import run
from py_linq import Enumerable
from hashlib import sha256
import tempfile


@dataclass
class Chart:
    chart: str
    binary: str = "helm"
    cluster_version: str = ""
    caches: Dict[str, str] = field(default_factory=dict, init=False)

    def _get_cache_key(self, *values: Dict[str, Any]):
        values_yaml = yaml.safe_dump_all(values)
        sha256_hash = sha256(values_yaml.encode("utf-8")).hexdigest()
        return sha256_hash

    def _get_from_cache(self, *values: Dict[str, Any]):
        cache_key = self._get_cache_key(*values)
        if cache_key not in self.caches:
            return None

        with open(self.caches[cache_key], "r") as f:
            return f.read().decode("utf-8")

    def _set_into_cache(self, rendered: str, *values: Dict[str, Any]):
        cache_key = self._get_cache_key(*values)
        with tempfile.TemporaryFile() as f:
            f.write(rendered.encode("utf-8"))
            self.caches[cache_key] = f.name

    def _render_by_helm(self, *values: Dict[str, Any]):
        cmds = [self.binary, "template", self.chart]

        with tempfile.TemporaryDirectory() as tmpdir:
            for index, value in enumerate(values):
                value_file = f"{tmpdir}/values-{index}.yaml"
                cmds.extend([f"-f", value_file])
                with open(value_file, "w") as f:
                    yaml.safe_dump(value, f)

            command = run(cmds)
            assert command.return_code == 0, command.err
            return command.out

    def render(self, *values: Dict[str, Any]):
        rendered = self._get_from_cache(*values)
        if rendered is None:
            rendered = self._render_by_helm(*values)
            self._set_into_cache(rendered, *values)

        return Enumerable(yaml.safe_load_all(rendered))
