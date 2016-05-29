import os
import sys
import tty
from subprocess import Popen
from select import select


def main():
    master, slave = os.openpty()
    stdin = sys.stdin.fileno()
    stdout = sys.stdout.fileno()

    try:
        tty.setraw(sys.stdout)

        process = Popen(
            args=["/bin/bash"],
            stdin=slave,
            stdout=slave,
            stderr=slave,
            close_fds=True,
            start_new_session=True,
        )

        while True:
            if process.poll() is not None:
                break

            r, _, _ = select([master, sys.stdin], [], [], 0.2)

            if master in r:
                os.write(stdout, os.read(master, 1024))
            if sys.stdin in r:
                os.write(master, os.read(stdin, 1024))
    finally:
        os.close(master)
        os.close(slave)
