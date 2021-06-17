import io
import runpy
import socket
import sys
from contextlib import redirect_stderr

import pydevd_pycharm
import waiting

from ._logger import log


class PycharmRemoteDebugger:
    DEFAULT_CONNECTION_TIMEOUT = 30

    def __init__(self, remote_machine: str, port: int, module: str = None, optional=False) -> None:
        self._remote_machine: str = remote_machine
        self._port: int = port
        self._module = module
        self._optional = optional

    def _debugger_login(self) -> bool:
        f = io.StringIO()

        with redirect_stderr(f):
            try:
                log.info(f"Attempting to connect to remote IDE {self._remote_machine}:{self._port}")
                pydevd_pycharm.settrace(self._remote_machine, port=self._port, stdoutToServer=True, stderrToServer=True)
                log.info(f"Debugger connected to IDE successfully")
                return True
            except ConnectionRefusedError as e:
                log.error(f"Error occurred while connecting to remote IDE, {e}")
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
            log.error(f"Timeout reached after {timeout} seconds")
            if not self._optional:
                raise

        if self._module is not None:
            self.run_module()

    def run_module(self):
        log.info(f"Running module {self._module[0]} with args {self._module[1:]}")
        argv = list(sys.argv)
        sys.argv = argv[argv.index("-m") + 1:]

        try:
            run_module_as_main = runpy._run_module_as_main
        except AttributeError:
            log.warning("Can't find runpy._run_module_as_main module.")
            runpy.run_module(self._module[0], alter_sys=True)
        else:
            run_module_as_main(self._module[0], alter_argv=True)

        sys.argv = argv
