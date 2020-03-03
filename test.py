import argparse
import os
import collections
import time
from subprocess import Popen, PIPE


def disk_usage(path):
    if hasattr(os, 'statvfs'):  # POSIX
        diskusage = collections.namedtuple('usage', 'total used free')
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return diskusage(total, used, free)
    else:
        raise Exception("System is not POSIX")


def detect_mount(path_to_mount):
    p = Popen("df -l | grep '^/dev' | awk '{print $1\":\"$6}'", stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    output, err = p.communicate()
    if p.returncode:
        raise Exception(f"Detected mount disk finished with error: {err}")
    data = dict([tuple(i.split(':')) for i in output.strip().split('\n')])

    if path_to_mount not in data.keys():
        raise Exception("Provided path is not mount")
    return data.get(path_to_mount)


def check_params(path_to_mount, count_files, size_files, free_space):

    if count_files * size_files > free_space:
        raise Exception("count*size of files more then free_space")
    disk = disk_usage(path_to_mount)
    print(f"Free Space on disk: {disk.free}")

    if disk.free <= free_space:
        raise Exception("Not enough free_space")


def write_files(mount_path, count_files, size_files):
    for i in range(count_files):
        f = open(os.path.join(mount_path, str(i)), "wb")
        f.seek(size_files - 1)
        f.write(b"\0")
        f.close()


def dd_files(mount_path, count_files, size_files):
    for i in range(count_files):
        start = time.time()
        cmd = ['dd', 'if=/dev/urandom', f"of={os.path.join(mount_path, str(i))}", f'bs={size_files}', 'count=1']
        p = Popen(cmd)
        output, err = p.communicate()
        if  p.returncode:
            print (f"dd Error: {err}")
        end = time.time()
        print(f"process {i} tool {end - start}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Path to mounted dist",
                        type=str, required=True)
    parser.add_argument("-X", "--free_space", help="Provide needed free space",
                        type=int, required=True)
    parser.add_argument("-Z", "--count_files", help="Count files",
                        type=int, required=True)
    parser.add_argument("-Y", "--size_files", help="Size of files in bytes",
                        type=int, required=True)

    args = parser.parse_args()

    count_files = args.count_files
    free_space = args.free_space
    size_files = args.size_files
    mount_path = args.path

    real_path = detect_mount(mount_path)
    check_params(real_path, count_files, size_files, free_space)
    write_files(real_path, count_files, size_files)
    dd_files(real_path, count_files, size_files)
