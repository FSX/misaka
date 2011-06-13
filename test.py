# -*- coding: utf8 -*-

import pantyshot as p

print('')

text = '''

# 裙底風光

裙底風光（又叫作裙底春、裙底春光等）是一個俚語，通常是指人們從婦女裙子底下由下往上仰視所看見或攝
得的影像照片。在這種情況下，觀看者可能會看見包括內衣、臀部，甚至是更私密的女陰。不過「裙底風光」
不一定只是指攝影照片而已，它也可以是指視訊、圖畫，或者僅僅就是以肉眼觀看這類景像。

擁有裙底風光的照片或視訊影片已經作為色情產業上的長期代表之一，往往在許多色情網站中十分常見。
瀏覽者可以免費或者網路付費的方式觀看這些拍攝下來的照片或影像，而此時裙底遭偷拍攝的少女或者婦女
往往處於完全不知情的情況下。


# Markdown extensions

Here are some demonstrations of Markdown "extensions".

An url: http://example.com

Test Smartypants: <3/4ths> -- Test test


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
    p.EXT_TABLES | p.EXT_STRIKETHROUGH | p.EXT_LAX_HTML_BLOCKS | p.EXT_AUTOLINK,
    p.HTML_EXPAND_TABS | p.HTML_TOC | p.HTML_SMARTYPANTS
)
#result = p.toc(text)
print(result)
