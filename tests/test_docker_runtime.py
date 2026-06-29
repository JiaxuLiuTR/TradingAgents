from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_docker_entrypoint_prepares_bind_mounted_output_dirs_before_app_start():
    """Bind-mounted host output dirs can be root-owned, so startup must fix them."""
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    entrypoint = ROOT / "docker-entrypoint.sh"

    assert 'ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]' in dockerfile
    assert 'CMD ["tradingagents"]' in dockerfile
    assert entrypoint.exists()

    script = entrypoint.read_text(encoding="utf-8")
    assert "/home/appuser/.tradingagents" in script
    assert "/home/appuser/app/reports" in script
    assert "chown -R appuser:appuser" in script
    assert 'set -- tradingagents "$@"' in script
    assert "exec runuser -u appuser --" in script
