from dataclasses import dataclass
import tempfile
from typing import Dict, Any
import yaml
from delegator import run
from py_linq import Enumerable


@dataclass
class Chart:
    chart: str
    binary: str = "helm"

    def render(self, *values: Dict[str, Any]):
        cmds = [self.binary, "template", self.chart]

        with tempfile.TemporaryDirectory() as tmpdir:
            for index, value in enumerate(values):
                value_file = f"{tmpdir}/values-{index}.yaml"
                cmds.extend([f"-f", value_file])
                with open(value_file, "w") as f:
                    yaml.safe_dump(value, f)

            command = run(cmds)

            assert command.return_code == 0, command.err

        return Enumerable(yaml.safe_load_all(command.out))
