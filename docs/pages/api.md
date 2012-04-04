---
layout: page.html
location: api
title: API
toc: true
---

Listings and descriptions of all constants, functions, classes and methods. This
page only describes the public objects, see the manual for usage examples.

If there is no list of arguments/parameters or no description of what the function
or method returns it does not accept or return anything.


## Markdown Extensions

 - **EXT_NO_INTRA_EMPHASIS** --- Do not parse emphasis inside of words. Strings
   such as `foo_bar_baz` will not generate `<em>` tags.

 - **EXT_TABLES** --- Parse [PHP-Markdown tables][].

 - **EXT_FENCED_CODE** --- Parse fenced code blocks, PHP-Markdown style. Blocks
   delimited with 3 or more `~` or backticks will be considered as code, without
   the need to be indented. An optional language name may be added at the end of
   the opening fence for the code block.

 - **EXT_AUTOLINK** --- Parse links even when they are not enclosed in `<>` characters.
   Autolinks for the http, https and ftp protocols will be automatically detected.
   Email addresses are also handled, and http links without protocol, but starting
   with `www`.

 - **EXT_STRIKETHROUGH** --- Parse strikethrough, PHP-Markdown style Two `~`
   characters mark the start of a strikethrough, e.g. `this is ~~good~~ bad`.

 - **EXT_LAX_HTML_BLOCKS** --- HTML blocks do not require to be surrounded by an empty
   line as in the Markdown standard.

 - **EXT_SPACE_HEADERS** --- A space is always required between the hash at the
   beginning of a header and its name, e.g. `#this is my header` would not be a
   valid header.

 - **EXT_SUPERSCRIPT** --- Parse superscripts after the `^` character; contiguous
   superscripts are nested together, and complex values can be enclosed in
   parenthesis, e.g. `this is the 2^(nd) time`.

[PHP-Markdown tables]: http://michelf.com/projects/php-markdown/extra/#table


## HTML Render Flags

 - **HTML_SKIP_HTML** --- Do not allow any user-inputted HTML in the output.

 - **HTML_SKIP_STYLE** --- Do not generate any `<style>` tags.

 - **HTML_SKIP_IMAGES** --- Do not generate any `<img>` tags.

 - **HTML_SKIP_LINKS** --- Do not generate any `<a>` tags.

 - **HTML_EXPAND_TABS** --- Unused.

 - **HTML_SAFELINK** --- Only generate links for protocols which are considered safe.

 - **HTML_TOC** --- Add HTML anchors to each header in the output HTML, to allow
   linking to each section.

 - **HTML_HARD_WRAP** --- Insert HTML `<br>` tags inside on paragraphs where the
   origin Markdown document had newlines (by default, Markdown ignores these newlines).

 - **HTML_USE_XHTML** --- Output XHTML-conformant tags.

 - **HTML_ESCAPE** --- `HTML_ESCAPE` overrides `SKIP_HTML`, `SKIP_STYLE`, `SKIP_LINKS`
   and `SKIP_IMAGES`. It doens't see if there are any valid tags, just escape all of them.

The following two flags are only for `misaka.html`.

 - **HTML_SMARTYPANTS** --- Post-process rendered markdown text with [SmartyPants][].

  [SmartyPants]: http://daringfireball.net/projects/smartypants/


 - **HTML_TOC_TREE** --- Render a table of contents.


## Render Flags

Constants that can be used in custom renderers.

 - **TABLE_ALIGN_L**
 - **TABLE_ALIGN_R**
 - **TABLE_ALIGN_C**
 - **TABLE_ALIGNMASK**
 - **TABLE_HEADER**


## html

Convert markdown text to (X)HTML.

Returns a unicode string.

 - **text** --- A byte or unicode string.
 - **extensions** --- Enable additional Markdown extensions with the `EXT_*` constants.
 - **render_flags** --- Adjust HTML rendering behaviour with the `HTML_*` constants.


## Smartypants

Smartypants is a post-processor for (X)HTML renderers and can be used standalone
or as a mixin. It adds a methode named `postprocess` to the renderer.

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


### postprocess

Process the input text.

Returns a unicode string.

 - **text** --- A byte or unicode string.


## BaseRenderer

The `BaseRenderer` is boilerplate code for creating your own renderers by
sublassing `BaseRenderer`. It takes care of setting the callbacks and flags.

 - **flags** --- Available as a read-only, integer type attribute named `self.flags`.


### setup

A method that can be overridden by the renderer that sublasses `BaseRenderer`.
It's called everytime an instance of a renderer is created.


## HtmlRenderer

The HTML renderer that's included in Sundown.

Do you override the `setup` method when subclassing `HtmlRenderer`. If you do
make sure to call parent class' `setup` method first.

 - **flags** --- Adjust HTML rendering behaviour with the `HTML_*` constants.


## HtmlTocRenderer

The HTML table of contents renderer that's included in Sundown.

Do you override the `setup` method when subclassing `HtmlTocRenderer`. If you do
make sure to call parent class' `setup` method first.

 - **flags** --- Adjust HTML rendering behaviour with the `HTML_*` constants.


## Markdown

The Markdown parser.

 - **renderer** --- An instance of `BaseRenderer`.
 - **extensions** --- Enable additional Markdown extensions with the `EXT_*` constants.


### render

Render the Markdon text.

Returns a unicode string.

 - **text** --- A byte or unicode string.
