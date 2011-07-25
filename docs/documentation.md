## Introduction

Misaka is a Python (2.7 and 3.2) binding for [Sundown][-1]. And
Sundown is a Markdown library written in C and it's really fast. Here is a
[benchmark][0]:

    Parsing the Markdown Syntax document 10000 times...
    Misaka: 3.34s
    Markdown: 486.86s
    Markdown2: 677.55s
    cMarkdown: 7.05s
    Discount: 16.76s

Python 2.7 was used in the benchmark. Besides Markdown (Python-Markdown) I
haven't been able to find any working Markdown parsers for Python 3. If there
are more, please notify me.


 [-1]: https://github.com/tanoku/sundown
 [0]: https://github.com/FSX/misaka/blob/master/benchmark/benchmark.py


## Installation

Download Misaka from [Github][1] and run the following command. Keep in mind
that Misaka has only been tested with Python 2.7 and 3.2.

    python setup.py install

Or from PyPi:

    pip install misaka

And you're done.


 [1]: https://github.com/FSX/misaka


## Usage

Example:

~~~~ {.python}
import misaka

print misaka.html('Hello, world!')
~~~~

With extensions and render flags:

~~~~ {.python}
import misaka as m

print m.html(
    'Hello, world!',
    m.EXT_AUTOLINK | m.EXT_TABLES,
    m.HTML_EXPAND_TABS
)
~~~~

In combination with `functools.partial`:

~~~~ {.python}
import functools
import misaka as m

markdown = functools.partial(
    m.html,
    extensions=m.EXT_AUTOLINK | m.EXT_TABLES,
    render_flags=m.HTML_EXPAND_TABS
)
print markdown('Awesome!')
~~~~

Or generate a table of contents:

~~~~ {.python}
sometext = '''
# Header one

Some text here.

## Header two

Some more text
'''

# To generate the TOC tree
print misaka.html(sometext,
    render_flags=misaka.HTML_TOC_TREE)

# To generate the HTML with the
#headers adjusted for the TOC
print misaka.html(sometext,
    render_flags=misaka.HTML_TOC)
~~~~

<div class="note">
    <p><b>Note:</b><br />
    When using fenced codeblocks you should also include <code>EXT_FENCED_CODE</code>
    when you generate a TOC tree. Otherwise code inside the fenced codeblocks
    that look like Markdown headers are also included in the TOC tree.</p>
</div>


## Syntax highlighting

Misaka and Sundown do not have syntax highlighting by default. With the fenced
codeblock extension and the the Github codeblock renderflag you can add classes
or a language attribute to codeblocks.

With the following snippet you can highlight codeblocks with [Pygments][2] by
passing HTML through it.

~~~~ {.python}
import re

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


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
~~~~

It looks for all codeblocks and either uses the language attribute or the first
class in the class attribute. It assumes that all the HTML is correct and no
no nesting of codeblocks occur.

The unescaping function is needed to unescape the code before Pygments procecesses
it. Otherwise you'll get double escape HTML.

 [2]: http://pygments.org/


## API

All of the following functions and constants are from the `misaka` module.


### misaka.html

The `html` function converts the Markdown text to HTML. It accepts the following arguments.

 * `text`: The Markdown source text.
 * `extensions`: One or more extension constants (optional).
 * `render_flags`: One or more render flag constants (optional).


### Extensions

The functionality of the following constants is explained at *Markdown Extensions*.

    EXT_AUTOLINK
    EXT_LAX_HTML_BLOCKS
    EXT_TABLES
    EXT_NO_INTRA_EMPHASIS
    EXT_STRIKETHROUGH
    EXT_FENCED_CODE
    EXT_SPACE_HEADERS
    EXT_SUPERSCRIPT


### Render Flags

The functionality of the following constants is explained at *Render Flags*.


    HTML_GITHUB_BLOCKCODE
    HTML_SKIP_HTML
    HTML_SKIP_STYLE
    HTML_HARD_WRAP
    HTML_TOC
    HTML_SKIP_LINKS
    HTML_SAFELINK
    HTML_SKIP_IMAGES
    HTML_EXPAND_TABS
    HTML_USE_XHTML
    HTML_SMARTYPANTS
    HTML_TOC_TREE


## Changelog

### 0.4.0 (2011-07-25)

 * API change: `misaka.toc` has been removed. Instead `HTML_TOC_TREE` has to be
   passed with `misaka.html` to get a TOC tree. When `HTML_TOC` is used the
   text will be rendered as usual, but the header HTML will be adjusted for the
   TOC.
 * Updated Sundown files; See commits from 2011-07-22 to 2011-07-24:
   https://github.com/tanoku/sundown/commits/master/
 * Added support for the Superscript extension.

### 0.3.3 (2011-07-22)

 * Fix a typo in README.txt. (heintz)
 * Fix non-NULL-terminated `kwlist` in `misaka_html`. (heintz)
 * Rename pantyshot to misaka in benchmark.py. (honza)
 * Renamed Upskirt to Sundown and updated the source files from 2011-07-04
   to 2011-07-19: https://github.com/tanoku/sundown/commits/master

### 0.3.2 (2011-07-03)

 * Fixed minor error in setup.py.

### 0.3.1 (2011-07-03)

 * Renamed Pantyshot to Misaka.
 * Updated Upskirt files; See commits from 2011-06-06 to 2011-06-23:
   https://github.com/tanoku/upskirt/commits/master/

### 0.3.0 (2011-06-16)

 * Added Python 3 support.
 * Updated Upskirt files; See commits from 2011-06-05 to 2011-06-09:
   https://github.com/tanoku/upskirt/commits/master/

### 0.2.1 (2011-06-05)

 * Updated Upskirt files; See commits from 2011-05-18 to 2011-06-02:
   https://github.com/tanoku/upskirt/commits/master/

### 0.2.0 (2011-05-17)

 * Added Smartypants render flag.
 * Added a `toc` function that outputs a table of contents.
 * Renamed `markdown` function to `html`.
 * Updated Upskirt files; See commits from 2011-05-02 to 2011-05-17:
   https://github.com/tanoku/upskirt/commits/master/

### 0.1.1 (2011-05-01)

 * Updated Upskirt files; a HTML escaping bug in the XHTML renderer was fixed.

### 0.1.0 (2011-05-01)

 * Initial release.


## License

Copyright (C) 2011 by Frank Smit <frank@61924.nl>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
