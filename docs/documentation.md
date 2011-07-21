## Introduction

Misaka is a Python (2.7 and 3.2) binding for [Sundown][-1]. And
Sundown is a Markdown library written in C and it's really fast. Here is a
[benchmark][0]:

    Misaka: 0.040000s
    Markdown: 4.900000s
    markdown2: 7.210000s
    cMarkdown: 0.070000s
    discount: 0.160000s

Python 2.7 was used in the benchmark. I couldn't find any working Markdown
parsers for Python 3. Is Misaka the only one?


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

misaka.html('Hello, world!')
~~~~

With extensions and render flags:

~~~~ {.python}
import misaka as m

m.html(
    'Hello, world!',
    m.EXT_AUTOLINK | m.EXT_TABLES,
    m.HTML_EXPAND_TABS<
)
~~~~

In combination with functools.partial:

~~~~ {.python}
import functools
import misaka as m

markdown = functools.partial(
    m.html,
    extensions=m.EXT_AUTOLINK | m.EXT_TABLES,
    render_flags=m.HTML_EXPAND_TABS
)
markdown('Awesome!')
~~~~

Or generate a table of contents:

~~~~ {.python}
misaka.toc('''
# Header one

Some text here.

## Header two

Some more text
''')
~~~~


## API

All of the following functions and constants are from the `misaka` module.


### misaka.html

The `html` function converts the Markdown text to HTML. It accepts the following arguments.

 * `text`: The Markdown source text.
 * `extensions`: One or more extension constants (optional).
 * `render_flags`: One or more render flag constants (optional).


### misaka.toc

The `toc` function generates a table of contents and accepts the following argument.

 * `text`: The Markdown source text.


### Extensions

The functionality of the following constants is explained at *Markdown Extensions*.

    EXT_AUTOLINK
    EXT_LAX_HTML_BLOCKS
    EXT_TABLES
    EXT_NO_INTRA_EMPHASIS
    EXT_STRIKETHROUGH
    EXT_FENCED_CODE
    EXT_SPACE_HEADERS


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


## Changelog

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
