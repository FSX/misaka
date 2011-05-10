# -*- coding: utf8 -*-

import pantyshot as p

print

text = '''

# Markdown extensions

Here are some demonstrations of Markdown extensions.


## MKDEXT_NO_INTRA_EMPHASIS

Lorem ipsum _d _olo_ r_ sit amet, __consectetur__ adipiscing _elit_.


## MKDEXT_TABLES

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |



## MKDEXT_FENCED_CODE

This is a paragraph introducing:

~~~~~~~~~~~~~~~~~~~~~
a one-line code block
~~~~~~~~~~~~~~~~~~~~~


## MKDEXT_AUTOLINK

Here is an URL: http://github.com/


## MKDEXT_STRIKETHROUGH


Nullam tincidunt dui ~vitae~ nulla ~~tristique~~ ultricies.


## MKDEXT_LAX_HTML_BLOCKS

<div>Donec quis lacus arcu, nec venenatis dolor. **Suspendisse** nibh eros, _pretium_ in vestibulum non, ultrices sed erat.</div>


<span>Donec quis lacus arcu, nec venenatis dolor. **Suspendisse** nibh eros, _pretium_ in vestibulum non, ultrices sed erat.</span>

<p>Donec quis lacus arcu, nec venenatis dolor. **Suspendisse** nibh eros, _pretium_ in vestibulum non, ultrices sed erat.</p>

<strong>Donec quis lacus arcu, nec venenatis dolor. **Suspendisse** nibh eros, _pretium_ in vestibulum non, ultrices sed erat.</strong>

'''

result = p.html(
    text,
    p.EXT_TABLES | p.EXT_STRIKETHROUGH | p.EXT_LAX_HTML_BLOCKS,
    p.HTML_SKIP_HTML | p.HTML_EXPAND_TABS | p.HTML_SKIP_LINKS | p.HTML_TOC
)
result = p.toc(text)
print result
