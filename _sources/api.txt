.. _api:

API
===

This page describes all classes, functions and constants. Usage examples
(renderer classes and pre- and post-processors) can be found at the
:doc:`/examples` page.

.. module:: misaka


Constants
---------

:py:class:`Markdown` parser extensions.

.. py:data:: EXT_NO_INTRA_EMPHASIS

   Do not parse emphasis inside of words. Strings such as ``foo_bar_baz`` will
   not generate `<em>` tags.

.. py:data:: EXT_TABLES

   Parse PHP-Markdown tables_.

.. py:data:: EXT_FENCED_CODE

   Parse fenced code blocks, PHP-Markdown style. Blocks delimited with 3 or
   more ``~`` or backticks will be considered as code, without the need to be
   indented. An optional language name may be added at the end of the opening
   fence for the code block.

.. py:data:: EXT_AUTOLINK

   Parse links even when they are not enclosed in ``<>`` characters. Autolinks
   for the http, https and ftp protocols will be automatically detected. Email
   addresses are also handled, and http links without protocol, but starting
   with ``www``.

.. py:data:: EXT_STRIKETHROUGH

   Parse strikethrough, PHP-Markdown style Two ``~`` characters mark the start
   of a strikethrough, e.g. ``this is ~~good~~ bad``.

.. py:data:: EXT_LAX_HTML_BLOCKS

   HTML blocks do not require to be surrounded by an empty line as in the
   Markdown standard.

.. py:data:: EXT_SPACE_HEADERS

   A space is always required between the hash at the beginning of a header and
   its name, e.g. ``#this is my header`` would not be a valid header.

.. py:data:: EXT_SUPERSCRIPT

   Parse superscripts after the ``^`` character; contiguous superscripts are
   nested together, and complex values can be enclosed in parenthesis,
   e.g. ``this is the 2^(nd) time``.

----

HTML render flags for :py:class:`HtmlRenderer` and :py:class:`HtmlTocRenderer`.

.. py:data:: HTML_SKIP_HTML

   Do not allow any user-inputted HTML in the output.

.. py:data:: HTML_SKIP_STYLE

   Do not generate any ``<style>`` tags.

.. py:data:: HTML_SKIP_IMAGES

   Do not generate any ``<img>`` tags.

.. py:data:: HTML_SKIP_LINKS

   Do not generate any ``<a>`` tags.

.. py:data:: HTML_EXPAND_TABS

   Unused.

.. py:data:: HTML_SAFELINK

   Only generate links for protocols which are considered safe.

.. py:data:: HTML_TOC

   Add HTML anchors to each header in the output HTML, to allow linking to
   each section.

.. py:data:: HTML_HARD_WRAP

   Insert HTML ``<br>`` tags inside on paragraphs where the origin Markdown
   document had newlines (by default, Markdown ignores these newlines).

.. py:data:: HTML_USE_XHTML

   Output XHTML-conformant tags.

.. py:data:: HTML_ESCAPE

   ``HTML_ESCAPE`` overrides ``SKIP_HTML``, ``SKIP_STYLE``, ``SKIP_LINKS`` and
   ``SKIP_IMAGES``. It doens't see if there are any valid tags, just escape all
   of them.

----

Constants for the :py:func:`html` function.

.. py:data:: HTML_SMARTYPANTS

   Post-process rendered markdown text with SmartyPants_.

.. py:data:: HTML_TOC_TREE

   Render a table of contents.

----

Constants that can be used in custom renderers.

.. py:data:: TABLE_ALIGN_L
.. py:data:: TABLE_ALIGN_R
.. py:data:: TABLE_ALIGN_C
.. py:data:: TABLE_ALIGNMASK
.. py:data:: TABLE_HEADER


.. _tables: http://michelf.com/projects/php-markdown/extra/#table
.. _codeblocks: http://michelf.com/projects/php-markdown/extra/#fenced-code-blocks
.. _SmartyPants: http://daringfireball.net/projects/smartypants/


Shorthand
---------

.. py:function:: html(text, extensions=0, render_flags=0)

   Convert markdown text to (X)HTML::

       misaka.html('source *text*',
           extensions=EXT_AUTOLINK|EXT_SUPERSCRIPT|EXT_STRIKETHROUGH,
           render_flags=HTML_SKIP_HTML|HTML_USE_XHTML)

   :param text: text as a (unicode) string.
   :param extensions: enable additional Markdown extensions with the
                      ``EXT_*`` constants.
   :param render_flags: adjust rendering behaviour with the ``HTML_*`` constants.


Post-processors
---------------

.. py:class:: SmartyPants()

   Smartypants post-processor for renderers. It can be used like this::

       class BleepRenderer(HtmlRenderer, SmartyPants):
           pass


   .. py:function:: postprocess(text)

      Process input text.

      :param text: text as a (unicode) string.


Renderers
---------

.. py:class:: BaseRenderer(flags=0)

   The ``BaseRenderer`` class does nothing by itself. It should be subclassed.

   :param flags: flags that can be used by the renderer.


   .. py:function:: setup()

      The ``setup`` method can be overridden by a subclass. This method
      is executed when a new object of the class is created. Right after
      ``__init__``.


.. py:class:: HtmlRenderer(flags=0)

   A HTML renderer.

   :param flags: Accepts the ``HTML_*`` constants as flags.


.. py:class:: HtmlTocRenderer(flags=0)

   A HTML table of contents renderer.

   :param flags: Accepts the ``HTML_*`` constants as flags.


Parser
------

.. py:class:: Markdown(renderer, extensions=0)

   The Markdown parser.

   :param renderer: an instance of ``BaseRenderer``.
   :param extensions: enable Markdown extensions with the ``EXT_*`` constants.


   .. py:function:: render(text)

      Render the given source text.

      :param text: text as a (unicode) string.
