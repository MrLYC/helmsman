from dataclasses import dataclass
import tempfile
from typing import Dict, Any
import yaml
from py_linq import Enumerable
from subprocess import Popen, PIPE


class ProcessRunException(Exception):
    pass


@dataclass
class Chart:
    chart: str
    binary: str = "helm"
    kube_version: str = ""
    api_version: str = ""

    def _render_by_helm(self, *values: Dict[str, Any]):
        cmds = [self.binary, "template", self.chart]

        if self.kube_version:
            cmds.append(f"--kube-version={self.kube_version}")

        if self.api_version:
            cmds.append(f"--api-version={self.api_version}")

        with tempfile.TemporaryDirectory() as tmpdir:
            for index, value in enumerate(values):
                value_file = f"{tmpdir}/values-{index}.yaml"
                cmds.append(f"--values={value_file}")
                with open(value_file, "w") as f:
                    yaml.safe_dump(value, f)

            process = Popen(cmds, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()

        if process.poll() != 0:
            raise ProcessRunException(stderr)

        return stdout

    def render(self, *values: Dict[str, Any]):
        rendered = self._render_by_helm(*values)
        return Enumerable(yaml.safe_load_all(rendered))
