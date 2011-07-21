import lxml.etree as etree
from lxml.html.clean import clean_html

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

import misaka as m


def highlight_code(html):
    html = clean_html(html)
    root = etree.fromstring(html)
    for pre in root.iter('pre'):
        try:
            code = pre[0]
        except IndexError:
            continue
        language = code.get('class')
        if language is None:
            continue
        new_pre = etree.fromstring(highlight(code.text,
            get_lexer_by_name(language), HtmlFormatter()))
        root.replace(pre, new_pre)
    return etree.tostring(root)


if __name__ == '__main__':
    with open('./documentation.md', 'r') as fd:
        src =  fd.read().strip()

    html = m.html(src, m.EXT_AUTOLINK | m.EXT_FENCED_CODE, m.HTML_TOC)
    toc = m.toc(src)

    html = highlight_code(html)

    with open('template.html', 'r') as fd:
        tpl = fd.read().strip()

    tpl = tpl.replace('{{ navigation }}', toc, 1)
    tpl = tpl.replace('{{ content }}', html, 1)

    with open('index.html', 'w') as fd:
        fd.write(tpl)