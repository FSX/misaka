import re
import os.path as path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

import misaka as m


# Assumes there are no nested codeblocks
_re_codeblock = re.compile(r'<pre(?: lang="([a-z0-9]+)")?><code'
    '(?: class="([a-z0-9]+).*?")?>(.*?)</code></pre>',
    re.IGNORECASE | re.DOTALL)

def highlight_code(html):
    def _unescape_html(html):
        html = html.replace('&lt;', '<')
        html = html.replace('&gt;', '>')
        html = html.replace('&amp;', '&')
        return html.replace('&quot;', '"')
    def _highlight_match(match):
        language, classname, code = match.groups()
        if (language or classname) is None:
            return match.group(0)
        return highlight(_unescape_html(code),
            get_lexer_by_name(language or classname),
            HtmlFormatter())
    return _re_codeblock.sub(_highlight_match, html)


if __name__ == '__main__':
    with open(path.join(path.dirname(__file__), 'documentation.md'), 'r') as fd:
        src =  fd.read().strip()

    html = m.html(src, m.EXT_AUTOLINK | m.EXT_FENCED_CODE,
        m.HTML_TOC | m.HTML_GITHUB_BLOCKCODE)
    toc = m.html(src, m.EXT_FENCED_CODE, m.HTML_TOC_TREE)

    html = highlight_code(html)

    with open(path.join(path.dirname(__file__), 'template.html'), 'r') as fd:
        tpl = fd.read().strip()

    tpl = tpl.replace('{{ navigation }}', toc, 1)
    tpl = tpl.replace('{{ content }}', html, 1)

    with open(path.join(path.dirname(__file__), 'index.html'), 'w') as fd:
        fd.write(tpl)
