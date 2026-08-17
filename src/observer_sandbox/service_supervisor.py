"""Backward-compatible production service entrypoint.

A historical deployment installed a systemd unit that invokes
``python -m observer_sandbox.service_supervisor``. The canonical runtime now owns
its restart behavior directly through systemd and no longer needs an in-process
child supervisor. Keep this module as a thin compatibility shim so servers with
that historical unit still run exactly one canonical runtime process until the
unit can be replaced during privileged maintenance.
"""

from __future__ import annotations

from .service import main


if __name__ == "__main__":
    main()
