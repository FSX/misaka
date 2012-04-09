---
layout: page.html
location: manual
title: Manual
toc: true
---

Some usage examples of Misaka. Everything about the examples is explained here.
What's possible, how it works and what you get.


## Installation

Installation from [PyPi][]:

~~~ console
% pip install misaka
~~~

Or get the most recent version from [Github][]:

~~~ console
% git clone git://github.com/FSX/misaka.git
% cd misaka
% python setup.py install
~~~

Visual Studio's support for C is not optimal and most VS compilers are missing
`stdint.h`, which is needed to compile Misaka. This file can be downloaded
from [msinttypes][] and put into `C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\include`
for example.

`setup.py` has been extended with some extra commands:

    clean          - cleanup directories created by packaging and build processes
    compile_cython - compile Cython files(s) into C file(s)
    update_vendor  - update Sundown files. Use `git submodule foreach git pull` to the most recent files

For example:

~~~ console
% python setup.py compile_cython
running cython
compiling /home/frank/Code/misaka/src/misaka.pyx
~~~

For the `compile_cython` command you need to have Cython installed. And [Git][] needs to
be installed to make the `update_vendor` command effective.

You have to manually run `git submodule foreach git pull` before running the
`update_vendor` command so the most recent files are downloaded first.

To run the unit tests [HTML Tidy][] must be installed first.

    pacman -S tidyhtml # on Arch Linux
    sudo apt-get install tidy # on Ubuntu

And then:

~~~ console
cd tests
python misaka_test.py
~~~


  [PyPi]: http://pypi.python.org/pypi/misaka
  [Github]: https://github.com/FSX/misaka
  [Git]: http://git-scm.com/
  [msinttypes]: http://msinttypes.googlecode.com/svn/trunk/stdint.h


## Basic Usage

You can make it yourself really easy by using `misaka.html`.

~~~ python
import misaka as m

print m.html('A ~~complex~~ simple example.',
    extensions=m.EXT_STRIKETHROUGH)
# <p>A <del>complex</del> simple example.</p>
~~~

Add another extension has been added by using the [bitwise][] OR operator.

~~~ python
print m.html('The 2^(nd) ~~complex~~ simple example.',
    extensions=m.EXT_STRIKETHROUGH | m.EXT_SUPERSCRIPT)
# <p>The 2<sup>nd</sup> <del>complex</del> simple example.</p>
~~~

Adding render flags works in the same way as adding extensions. See the [API][]
documentation for a listing of Markdown extensions and HTML render flags.

~~~ python
print m.html('The 3^(nd) ~~complex~~ <i>simple</i> example.',
    extensions=m.EXT_STRIKETHROUGH | m.EXT_SUPERSCRIPT,
    render_flags=m.HTML_SKIP_HTML)
# <p>The 3<sup>nd</sup> <del>complex</del> simple example.</p>
~~~

The `<i>`'s from `<i>simple</i>` are not in the output.

  [bitwise]: http://docs.python.org/library/stdtypes.html#bitwise-operations-on-integer-types
  [API]: {{ get_url('/api') }}


## Custom Renderers

If you would like to influence the rendering or make a new renderer yourself,
don't wait and subclass `BaseRenderer` and start implementing your render
methods.

Here is a list of methods that can be implemented in a renderer. All method
arguments are prefixed with their type. A `bool` is a boolean, `int` an integer
and `str` a string or unicode string in Python 2. Remember that these methods are
going to be implemented in a class. So the first argument is always `self`. The
data that's returned from a render method should always be a byte or unicode string.

When an exception is raised in a render method a stacktrace will be shown in
STDOUT, but the rendering process will not stop. Instead the render method just
returns nothing.

**Block-level**:

~~~
block_code(str code, str language)
block_quote(str quote)
block_html(str raw_html)
header(str text, int level)
hrule()
list(str contents, bool is_ordered)
list_item(str text, bool is_ordered)
paragraph(str text)
table(str header, str body)
table_row(str content)
table_cell(str content, int flags)
~~~

The `flags` argument of the `table_cell` method can be compared with one of the
`TABLE_*` render flags. For example:

~~~ python
# Table cell is a header?
if flags & m.TABLE_HEADER:
    print 'This is a header cell'
else:
    print 'This is not a header cell'

# Alignment of the cell?
alignment = flags & m.TABLE_ALIGNMASK

if alignment == m.TABLE_ALIGN_C:
    print 'Center'
elif alignment == m.TABLE_ALIGN_L:
    print 'Left'
elif alignment == m.TABLE_ALIGN_R:
    print 'Right'
else:
    print 'Not aligned'
~~~

**Span-level**:

~~~
autolink(str link, bool is_email)
codespan(str code)
double_emphasis(str text)
emphasis(str text)
image(str link, str title, str alt_text)
linebreak()
link(str link, str title, str content)
raw_html(str raw_html)
triple_emphasis(str text)
strikethrough(str text)
superscript(str text)
~~~

**Low-level**:

~~~
entity(str text)
normal_text(str text)
~~~

**Header and footer of the document**:

~~~
doc_header()
doc_footer()
~~~

**Pre- and post-processing**:

~~~
preprocess(str full_document)
postprocess(str full_document)
~~~


### Code Highlighting

A simple code highlighting example with [Pygments][] and [Houdini.py][].

~~~ python
import houdini as h
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

# Create a custom renderer
class BleepRenderer(HtmlRenderer, SmartyPants):
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                h.escape_html(text.strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

# And use the renderer
renderer = BleepRenderer()
md = m.Markdown(renderer,
    extensions=m.EXT_FENCED_CODE | m.EXT_NO_INTRA_EMPHASIS)

print md.render('Some Markdown text.')
~~~

  [Pygments]: http://pygments.org/
  [Houdini.py]: http://python-houdini.61924.nl/


## Pre- & Postprocessors

Pre- and postprocessors are classes that implement `preprocess` and/or `postprocess`
methods. Both accept one argument. The source text is passed to `preprocess` and
the rendered text (e.g. HTML) is passed to `postprocess`.

Pre- and postprocessors are intended to be used as mixins as you can see in the
code highlighting example. `HtmlRenderer` and `SmartyPants` are both subclassed
by `BleepRenderer` and `SmartyPants` is mixin.

Here's a useless example:

~~~ python
class ExamplePreprocessor(object):
    def preprocess(self, text):
        return text.replace(' ', '_')

class BleepRenderer(HtmlRenderer, ExamplePreprocessor):
    pass
~~~

But you can also add a `preprocess` and/or `postprocess` to the renderer instead
of using a mixin class.

~~~ python
class BleepRenderer(HtmlRenderer):
    def preprocess(self, text):
        return text.replace(' ', '_')
~~~


### Smartypants

Smartypants is a post-processor for (X)HTML renderers and can be used standalone
or as a mixin. It adds a methode named `postprocess` to the renderer. It converts
the charachter sequences in the left column to the sequences in the right column.

Source                           | Result
---------------------------------|----------
`'s` (s, t, m, d, re, ll, ve) ^1 | &rsquo;s
`--`                             | &mdash;
`-`                              | &ndash;
`...`                            | &hellip;
`. . .`                          | &hellip;
`(c)`                            | &copy;
`(r)`                            | &reg;
`(tm)`                           | &trade;
`3/4`                            | &frac34;
`1/2`                            | &frac12;
`1/4`                            | &frac14;

1. A `'` followed by a `s`, `t`, `m`, `d`, `re`, `ll` or `ve` will be turned
   into `&rsquo;s`, `&rsquo;t`, and so on.
