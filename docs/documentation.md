## Introduction

Misaka is a Python (2.7 and 3.2) binding for [Sundown][1], a markdown library.
The binding is written in [Cython][2]/C and Sundown is written in C. So it's
very fast.

 [1]: https://github.com/tanoku/sundown
 [2]: http://cython.org/


## Installation

Misaka can be installed with:

    pip install misaka

Or if you want the latest copy from [Github][3]:

    git clone https://github.com/FSX/misaka.git
    cd misaka
    python setup.py install

Cython is not needed, because the generated C file is included. If you want to
use Cython and regenerate the C file you can user `setup_cython.py` instead of
`setup.py`.

 [3]: https://github.com/FSX/misaka


## Usage

Like this:

~~~~ {.python}
from misaka import Markdown, HtmlRenderer

md = Markdown(HtmlRenderer())

print md.render('some text')
~~~~

Or like this:

~~~~ {.python}
from misaka import Markdown, HtmlRenderer, SmartyPants

class BleepRenderer(HtmlRenderer, SmartyPants):
    pass

md = Markdown(BleepRenderer())

print md.render('some text')
~~~~


<div class="note">
    <p><b>Note:</b><br />
    When using fenced codeblocks you should also include <code>EXT_FENCED_CODE</code>
    when you generate a TOC tree. Otherwise code inside the fenced codeblocks
    that look like Markdown headers are also included in the TOC tree.</p>
</div>


## API

-


## Changelog

### 0.4.2 (2011-08-25)

 * Updated Sundown files; See commits from 2011-08-03 to 2011-08-09:
   https://github.com/tanoku/sundown/commits/master/

### 0.4.1 (2011-08-01)

 * Fixed buffer management. It was broken and leaked memory. (tanoku)
 * Updated Sundown files; See commits from 2011-07-29 to 2011-08-01:
   https://github.com/tanoku/sundown/commits/master/

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
