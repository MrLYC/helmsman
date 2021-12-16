"""Tests for `helmsman`.cli module."""
from typing import List

import pytest
from click.testing import CliRunner

import helmsman
from helmsman import cli


@pytest.mark.parametrize(
    "options,expected",
    [
        ([], "helmsman.cli.main"),
        (["--help"], "Usage: main [OPTIONS]"),
        (["--version"], f"main, version { helmsman.__version__ }\n"),
    ],
)
def test_command_line_interface(options: List[str], expected: str) -> None:
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, options)
    assert result.exit_code == 0
    assert expected in result.output
