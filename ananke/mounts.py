import os


def is_in_sshfs_cwd(child_pid):
    mounts = _read_sshfs_mounts(child_pid)
    cwd = _cwd(child_pid)
    if _cwd_in_mounts(cwd, mounts):
        return True
    return False


def _read_sshfs_mounts(child_pid):
    mounts = []

    with open("/proc/%s/mounts" % child_pid, "rb") as f:
        for line in f:
            parts = line.split(b" ")
            if parts[2] == b"fuse.sshfs":
                mounts.append(parts[1])

    return mounts


def _cwd(child_pid):
    return os.readlink("/proc/%s/cwd" % child_pid)


def _cwd_in_mounts(cwd, mounts):
    for mount in mounts:
        if mount.startswith(bytes(cwd, 'ascii')):
            return True

    return False
