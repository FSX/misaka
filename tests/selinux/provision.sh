#!/usr/bin/env sh

sudo apt-get --yes install \
    selinux-basics \
    selinux-policy-default \
    auditd

sudo selinux-activate

sudo apt-get --yes install \
    python3-dev \
    python3-setuptools \
    libffi-dev \
    tidy
