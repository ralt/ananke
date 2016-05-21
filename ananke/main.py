import os
import sys
from subprocess import Popen
from select import select


def main():
    master, slave = os.openpty()
    stdin = sys.stdin.fileno()
    stdout = sys.stdout.fileno()

    try:
        ttyname = os.ttyname(slave)

        def _preexec():
            os.setsid()
            open(ttyname, "r+")

        process = Popen(
            args=["/bin/bash"],
            preexec_fn=_preexec,
            stdin=slave,
            stdout=slave,
            stderr=slave,
            close_fds=True,
        )

        while True:
            if process.poll() is not None:
                break

            r, _, _ = select([master, sys.stdin], [], [])

            if master in r:
                os.write(stdout, os.read(master, 1024))
            if sys.stdin in r:
                os.write(master, os.read(stdin, 1024))
    finally:
        os.close(master)
        os.close(slave)
