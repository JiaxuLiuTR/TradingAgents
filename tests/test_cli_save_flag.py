from __future__ import annotations

from unittest import mock

import pytest
from typer.testing import CliRunner

import cli.main as m


@pytest.mark.parametrize(
    ("raw_args", "expected"),
    [
        (["--ticker", "SPY"], None),
        (["--ticker", "SPY", "--save"], True),
        (["--ticker", "SPY", "--no-save"], False),
    ],
)
def test_save_flag_is_forwarded_to_run_analysis(raw_args, expected):
    runner = CliRunner()

    with mock.patch.object(m, "run_analysis") as run_analysis:
        result = runner.invoke(m.app, raw_args)

    assert result.exit_code == 0
    assert run_analysis.call_args.kwargs["save"] is expected


@pytest.mark.parametrize(
    ("save", "non_interactive", "expected"),
    [
        (None, True, True),
        (None, False, None),
        (True, True, True),
        (True, False, True),
        (False, True, False),
        (False, False, False),
    ],
)
def test_resolve_save_report_preserves_defaults_and_honors_explicit_flags(
    save, non_interactive, expected
):
    assert m._resolve_save_report(save, non_interactive=non_interactive) is expected
