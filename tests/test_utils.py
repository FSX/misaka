# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE, STDOUT


def clean_html(dirty_html):
    input_html = dirty_html.encode('utf-8')
    p = Popen(['tidy', '--show-body-only', '1', '--quiet', '1', '--show-warnings', '0', '-utf8'],
        stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout, stderr = p.communicate(input=input_html)

    return stdout.decode('utf-8')
