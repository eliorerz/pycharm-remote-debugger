import io
import runpy
import socket
import sys
from contextlib import redirect_stderr
from enum import IntEnum
from typing import List

import pydevd_pycharm
import waiting

from ._logger import log


class CodeType(IntEnum):
    FILE = 0
    MODULE = 1


class PycharmRemoteDebugger:
    DEFAULT_CONNECTION_TIMEOUT = 30

    def __init__(self,
                 remote_machine: str,
                 port: int,
                 code_type: CodeType,
                 code_args: List[str] = None,
                 optional=False
                 ):

        self._remote_machine: str = remote_machine
        self._port: int = port
        self._code_type: CodeType = code_type
        self._code_args: List[str] = code_args
        self._optional: bool = optional

    def _debugger_login(self) -> bool:
        f = io.StringIO()

        with redirect_stderr(f):
            pydevd_pycharm.settrace(self._remote_machine, port=self._port, stdoutToServer=True, stderrToServer=True)
            log.info(f"Debugger connected to IDE successfully")
            return True

    def _wait_for_debugger(self, timeout=DEFAULT_CONNECTION_TIMEOUT):
        try:
            log.info(f"Trying to connect to the remote IDE {self._remote_machine}:{self._port}")
            waiting.wait(
                lambda: self._debugger_login(),
                timeout_seconds=timeout,
                sleep_seconds=1,
                waiting_for="remote debugger to be ready",
                expected_exceptions=(ConnectionRefusedError,)
            )
        except (socket.timeout, waiting.exceptions.TimeoutExpired):
            log.error(f"Error occurred while connecting to remote IDE. Timeout reached after {timeout} seconds.")
            if not self._optional:
                raise

    def _run_file(self):
        runpy.run_path(self._code_args[0], run_name="__main__")

    def _run_module(self):
        try:
            run_module_as_main = runpy._run_module_as_main
        except AttributeError:
            log.warning("Can't find runpy._run_module_as_main method.")
            runpy.run_module(self._code_args[0], alter_sys=True)
        else:
            run_module_as_main(self._code_args[0], alter_argv=True)

    def debug(self, timeout: int):
        self._wait_for_debugger(timeout)
        argv = list(sys.argv)
        log.info(f"Running {self._code_type.name.lower()} {self._code_args[0]} with args {self._code_args[1:]}")

        if self._code_args is not None:
            sys.argv = list(self._code_args)
            if self._code_type == CodeType.MODULE:
                self._run_module()
            elif self._code_type == CodeType.FILE:
                self._run_file()

        sys.argv = argv
