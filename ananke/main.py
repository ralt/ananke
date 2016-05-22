import pexpect


def filter():
    chunks = []

    def _filter(chunk):
        if ord(chunk) != 13:
            chunks.append(chunk)
            return chunk

        command = "".join(chunks)
        if command == "ls":
            return chr(29)

        while len(chunks) > 0:
            chunks.pop()

        return chunk

    return _filter


def main():
    c = pexpect.spawn("/bin/bash")
    c.interact(escape_character=chr(29), input_filter=filter())
