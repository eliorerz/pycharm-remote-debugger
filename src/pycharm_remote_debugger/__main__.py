import argparse

from ._pycharm_remote_debugger import PycharmRemoteDebugger, CodeType


def get_args():
    parser = argparse.ArgumentParser(description="Pycharm remote debugger")
    parser.add_argument("-r", "--remote", help="Remote machine address", type=str)
    parser.add_argument("-p", "--port", help="Remote debugger port", type=int)
    parser.add_argument("-o", "--optional", help="Continue if not able to connect to the remote debugger", nargs='?',
                        default=False, type=bool, const=True)
    parser.add_argument("-t", "--timeout", help="Connection timeout", type=int,
                        default=PycharmRemoteDebugger.DEFAULT_CONNECTION_TIMEOUT)
    parser.add_argument("-m", "--module", help="Module to run", type=str, nargs="...")
    parser.add_argument("script", nargs="...")
    args = parser.parse_args()

    if not args.port or not args.remote:
        raise ValueError("Missing remote IDE arguments - try: remote_debugger -r <remote_address> -p <port> ... ")

    if args.script is None and args.module is None:
        raise ValueError("Missing script path or module to execute")

    return args


def main():
    args = get_args()
    code_type = CodeType.MODULE if args.module else CodeType.FILE
    debugger = PycharmRemoteDebugger(args.remote, args.port, code_type, args.module or args.script, args.optional)
    debugger.debug(args.timeout)


if __name__ == '__main__':
    main()
