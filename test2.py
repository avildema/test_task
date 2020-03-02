import argparse
import os
from multiprocessing import Pool
from subprocess import check_output, STDOUT
from functools import partial


def run_process(server, command):
    out = check_output(f'ssh {server} "{command}"', stderr=STDOUT, shell=True)
    print(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command", help="Launch command",
                        type=str, required=True)
    parser.add_argument('-l', '--list', nargs='+',
                        help='List of servers', required=False)

    args = parser.parse_args()

    with Pool(processes=len(args.list)) as pool:
        pool.map(partial(run_process, command=args.command), args.list)

