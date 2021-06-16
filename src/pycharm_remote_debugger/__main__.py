import argparse

from .pycharm_remote_debugger import PycharmRemoteDebugger


def main():
    parser = argparse.ArgumentParser(description="Pycharm remote debugger")
    parser.add_argument("-r", "--remote", help="Remote machine address", type=str, default="")
    parser.add_argument("-p", "--port", help="Remote debugger port", type=int)
    parser.add_argument("-o", "--optional", help="Continue if not able to connect to the remote debugger", nargs='?',
                        default=False, type=bool, const=True)
    parser.add_argument("-t", "--timeout", help="Connection timeout", type=int,
                        default=PycharmRemoteDebugger.DEFAULT_CONNECTION_TIMEOUT)

    args = parser.parse_args()
    debugger = PycharmRemoteDebugger(args.remote, args.port, args.optional)
    debugger.wait_for_debugger(args.timeout)


if __name__ == '__main__':
    main()
