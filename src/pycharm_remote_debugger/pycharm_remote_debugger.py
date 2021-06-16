import io
import socket
from contextlib import redirect_stderr

import pydevd_pycharm
import waiting


class PycharmRemoteDebugger:
    DEFAULT_CONNECTION_TIMEOUT = 30

    def __init__(self, remote_machine: str, port: int, optional=False) -> None:
        self._remote_machine: str = remote_machine
        self._port: int = port
        self._optional = optional

    def _debugger_login(self) -> bool:
        f = io.StringIO()

        with redirect_stderr(f):
            try:
                pydevd_pycharm.settrace(self._remote_machine, port=self._port, stdoutToServer=True, stderrToServer=True)
                return True
            except ConnectionRefusedError:
                return False

    def wait_for_debugger(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
        try:
            waiting.wait(
                lambda: self._debugger_login(),
                timeout_seconds=timeout,
                sleep_seconds=1,
                waiting_for="remote debugger to be ready"
            )
        except socket.timeout:
            if not self._optional:
                raise
