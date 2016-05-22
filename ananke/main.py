import re

import pexpect

from .mounts import is_in_sshfs_cwd


def empty(list):
    while len(list) > 0:
        list.pop()


def filter(child_pid):
    chunks = []

    def _filter(chunk):
        if len(chunk) > 1 or ord(chunk) != 13:
            chunks.append(chunk)
            return chunk

        if is_in_sshfs_cwd(child_pid):
            # Don't prevent from going out of the folder.
            bytes_command = b""
            for c in chunks:
                bytes_command += c
            command = bytes_command.decode("ascii")
            if re.match(r"^cd\s*", command):
                empty(chunks)

                return chunk

            backspaces = b""
            for i in range(0, len(chunks)):
                backspaces += b"\b"

            empty(chunks)

            return backspaces

        empty(chunks)

        return chunk

    return _filter


def main():
    c = pexpect.spawn("/bin/bash")
    c.interact(escape_character=None, input_filter=filter(c.pid))
