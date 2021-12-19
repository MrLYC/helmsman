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
                cmds.append(f"-f={value_file}")
                with open(value_file, "w") as f:
                    yaml.safe_dump(value, f)

            command = run(cmds)
            assert command.return_code == 0, command.err
            return command.out

    def render(self, *values: Dict[str, Any]):
        rendered = self._render_by_helm(*values)
        return Enumerable(yaml.safe_load_all(rendered))
