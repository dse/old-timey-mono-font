#!/usr/bin/env -S python
import os, fcntl, struct, re

BUILD_NR_FILE = os.path.dirname(__file__) + "/../.test-build-number.txt"
LOCK_FILE     = os.path.dirname(__file__) + "/../.test-build-number.lock"

def main():
    get_lock()
    build_number = get_build_number()
    build_number += 1
    set_build_number(build_number)
    release_lock()
    print("%d" % build_number)

lock_fh = None
def get_lock():
    global lock_fh
    if lock_fh is not None:
        return
    lock_fh = open(LOCK_FILE, mode='w')
    fcntl.lockf(lock_fh.fileno(), fcntl.LOCK_EX)

def release_lock():
    global lock_fh
    if lock_fh is None:
        return
    fcntl.lockf(lock_fh.fileno(), fcntl.LOCK_UN)
    lock_fh.close()
    lock_fh = None

def get_build_number():
    if os.path.exists(BUILD_NR_FILE):
        fh = open(BUILD_NR_FILE, mode='r')
        build_number = fh.readline()
        fh.close()
        if match := re.search(r'\d+', build_number):
            try:
                return int(match.group(0))
            except ValueError:
                return 0
        else:
            return 0
    else:
        return 0

def set_build_number(build_number):
    fh = open(BUILD_NR_FILE, mode='w')
    fh.write("%d\n" % build_number)
    fh.close()

main()
