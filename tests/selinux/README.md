SELinux
=======

CFFI's [old-style callbacks][1] don't work on SELinux with enforcing
mode. [New-style callbacks][2] do work. This Vagrant configuration can
be used if Misaka work on SELinux with enforcing mode.

Only Vagrant and needs to be installed. `run_test_in_selinux.sh` does
the rest. :)

[1]: https://cffi.readthedocs.io/en/latest/using.html#callbacks-old-style
[2]: https://cffi.readthedocs.io/en/latest/using.html#extern-python-new-style-callbacks
