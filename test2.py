import argparse
import os
from multiprocessing import Pool
from subprocess import Popen, PIPE
from functools import partial


def run_process(server, command):
    p = Popen(f'ssh {server} "{command}"', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    output, err = p.communicate()
    if p.returncode:
        print (f"{command} on {server} finished incorrect: {err}")
    else:
        print(server, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command", help="Launch command",
                        type=str, required=True)
    parser.add_argument('-l', '--list', nargs='+',
                        help='List of servers', required=False)

    args = parser.parse_args()

    with Pool(processes=len(args.list)) as pool:
        pool.map(partial(run_process, command=args.command), args.list)
    pool.join()

