from . import const
from ._md4c import lib
from .api import Base
from .detail import BlockDetail, SpanDetail
from .utils import Buffer


class Html(Base):
    def __init__(self, parser_flags=None, render_flags=None):
        super().__init__(parser_flags)
        self.image_nesting_level = 0
        self.header_open_tags = (
            b'<h1>', b'<h2>', b'<h3>', b'<h4>', b'<h5>', b'<h6>',
        )
        self.header_close_tags = (
            b'</h1>\n', b'</h2>\n', b'</h3>\n', b'</h4>\n',
            b'</h5>\n', b'</h6>\n',
        )

    def enter_block(self, out, ntype, detail):
        if ntype == const.BLOCK_DOC:
            pass
        elif ntype == const.BLOCK_QUOTE:
            out.append(b'<blockquote>\n')
        elif ntype == const.BLOCK_UL:
            out.append(b'<ul>\n')
        elif ntype == const.BLOCK_OL:
            self.render_open_ol_block(out, detail)
        elif ntype == const.BLOCK_LI:
            self.render_open_li_block(out, detail)
        elif ntype == const.BLOCK_HR:
            out.append(b'<hr>\n')
        elif ntype == const.BLOCK_H:
            detail = BlockDetail.H.from_c(detail)
            out.append(self.header_open_tags[detail.level - 1])
        elif ntype == const.BLOCK_CODE:
            self.render_open_code_block(out, detail)
        elif ntype == const.BLOCK_HTML:
            pass
        elif ntype == const.BLOCK_P:
            out.append(b'<p>')
        elif ntype == const.BLOCK_TABLE:
            out.append(b'<table>\n')
        elif ntype == const.BLOCK_THEAD:
            out.append(b'<thead>\n')
        elif ntype == const.BLOCK_TBODY:
            out.append(b'<tbody>\n')
        elif ntype == const.BLOCK_TR:
            out.append(b'<tr>\n')
        elif ntype == const.BLOCK_TH:
            self.render_open_td_block(out, b'th', detail)
        elif ntype == const.BLOCK_TD:
            self.render_open_td_block(out, b'td', detail)

    def leave_block(self, out, ntype, detail):
        if ntype == const.BLOCK_DOC:
            pass
        elif ntype == const.BLOCK_QUOTE:
            out.append(b'</blockquote>\n')
        elif ntype == const.BLOCK_UL:
            out.append(b'</ul>\n')
        elif ntype == const.BLOCK_OL:
            out.append(b'</ol>\n')
        elif ntype == const.BLOCK_LI:
            out.append(b'</li>\n')
        elif ntype == const.BLOCK_HR:
            out.append(b'<hr>\n')
        elif ntype == const.BLOCK_H:
            detail = BlockDetail.H.from_c(detail)
            out.append(self.header_close_tags[detail.level - 1])
        elif ntype == const.BLOCK_CODE:
            out.append(b'</code></pre>\n')
        elif ntype == const.BLOCK_HTML:
            pass
        elif ntype == const.BLOCK_P:
            out.append(b'</p>\n')
        elif ntype == const.BLOCK_TABLE:
            out.append(b'</table>\n')
        elif ntype == const.BLOCK_THEAD:
            out.append(b'</thead>\n')
        elif ntype == const.BLOCK_TBODY:
            out.append(b'</tbody>\n')
        elif ntype == const.BLOCK_TR:
            out.append(b'</tr>\n')
        elif ntype == const.BLOCK_TH:
            out.append(b'</th>\n')
        elif ntype == const.BLOCK_TD:
            out.append(b'</td>\n')

    def enter_span(self, out, ntype, detail):
        if self.image_nesting_level > 0:
            return

        if ntype == const.SPAN_EM:
            out.append(b'<em>')
        elif ntype == const.SPAN_STRONG:
            out.append(b'<strong>')
        elif ntype == const.SPAN_A:
            self.render_open_a_span(out, detail)
        elif ntype == const.SPAN_IMG:
            self.render_open_img_span(out, detail)
        elif ntype == const.SPAN_CODE:
            out.append(b'<code>')
        elif ntype == const.SPAN_DEL:
            out.append(b'<del>')

    def leave_span(self, out, ntype, detail):
        if self.image_nesting_level > 0:
            if self.image_nesting_level == 1 and ntype == const.SPAN_IMG:
                self.render_close_img_span(out, detail)
            return

        if ntype == const.SPAN_EM:
            out.append(b'</em>')
        elif ntype == const.SPAN_STRONG:
            out.append(b'</strong>')
        elif ntype == const.SPAN_A:
            out.append(b'</a>')
        elif ntype == const.SPAN_IMG:
            pass  # Noop, handled above.
        elif ntype == const.SPAN_CODE:
            out.append(b'</code>')
        elif ntype == const.SPAN_DEL:
            out.append(b'</del>')

    def text(self, out, ntype, text):
        if ntype == const.TEXT_NULLCHAR:
            return '\x00'
        elif ntype == const.TEXT_BR:
            if self.image_nesting_level == 0:
                out.append(b'<br>\n')
            else:
                out.append(b' ')
        elif ntype == const.TEXT_SOFTBR:
            if self.image_nesting_level == 0:
                out.append(b'\n')
            else:
                out.append(b' ')
        elif ntype == const.TEXT_HTML:
            out.append(text)
        elif ntype == const.TEXT_ENTITY:
            out.append(render_entity(text, _escape_html))
        else:
            out.append(_escape_html(text))

    def debug(self, msg):
        print(f'DEBUG: {msg}')

    def render_open_ol_block(self, out, detail):
        detail = BlockDetail.Ol.from_c(detail)

        if detail.start == 1:
            out.append(b'<ol>\n')
        else:
            out.append(f'<ol start="{detail.start}">\n')

    def render_open_li_block(self, out, detail):
        detail = BlockDetail.Li.from_c(detail)

        if detail.is_task:
            out.append(
                b'<li class="task-list-item">'
                b'<input type="checkbox" class="task-list-item-checkbox" disabled'
            )
            if detail.task_mark == 'x' or detail.task_mark == 'X':
                out.append(b' checked')
            out.append(b'>')
        else:
            out.append(b'<li>')

    def render_open_code_block(self, out, detail):
        detail = BlockDetail.Code.from_c(detail)

        out.append(b'<pre><code')

        if detail.lang:
            lang = _render_attribute(detail.lang, _escape_html)
            out.append(' class="language-')
            out.append(lang)
            out.append('"')

        out.append(b'>')

    def render_open_td_block(self, out, cell_type, detail):
        detail = BlockDetail.Td.from_c(detail)

        out.append(b'<')
        out.append(cell_type)

        if detail.align == const.LEFT:
            out.append(b' align="left">')
        if detail.align == const.CENTER:
            out.append(b' align="center">')
        if detail.align == const.RIGHT:
            out.append(b' align="right">')
        else:
            out.append(b'>')

    def render_open_a_span(self, out, detail):
        detail = SpanDetail.A.from_c(detail)

        out.append(b'<a href="')
        out.append(_render_attribute(detail.href, _escape_url))

        if detail.title:
            out.append(b'" title="')
            out.append(_render_attribute(detail.title, _escape_html))

        out.append(b'">')

    def render_open_img_span(self, out, detail):
        detail = SpanDetail.Img.from_c(detail)

        out.append(b'<img src="')
        out.append(_render_attribute(detail.src, _escape_url))
        out.append(b'" alt="')

        self.image_nesting_level += 1

    def render_close_img_span(self, out, detail):
        detail = SpanDetail.Img.from_c(detail)

        if detail.title:
            out.append(b'" title="')
            out.append(_render_attribute(detail.title, _escape_html))

        out.append(b'">')
        self.image_nesting_level -= 1


def _escape_html(text):
    if isinstance(text, str):
        text = text.encode('utf-8')

    with Buffer(int(len(text) * 1.2)) as ob:
        lib.misaka_escape_html(ob._storage, text, len(text))
        return ob.to_str()


def _escape_url(text):
    if isinstance(text, str):
        text = text.encode('utf-8')

    with Buffer(int(len(text) * 1.2)) as ob:
        lib.misaka_escape_url(ob._storage, text, len(text))
        return ob.to_str()


def _codepoint_to_utf8(codepoint):
    with Buffer(4) as ob:
        lib.misaka_codepoint_to_utf8(ob._storage, codepoint)
        return ob.to_str()


def _render_attribute(attr, fn_escape):
    with Buffer(int(len(attr) * 1.2)) as ob:
        for p in attr.parts:
            if p.type == const.TEXT_NULLCHAR:
                ob.append(b'\x00')
            elif p.type == const.TEXT_ENTITY:
                ob.append(render_entity(p.text, fn_escape))
            else:
                ob.append(fn_escape(p.text))
        return ob.to_str()


def render_entity(text, fn_escape):
    # TODO: MD_RENDER_FLAG_VERBATIM_ENTITIES

    if len(text) > 3 and text[1] == '#':
        codepoint = 0
        if text[2] == 'x' or text[2] == 'X':
            codepoint = int(text[3:-1], 16)
        else:
            codepoint = int(text[2:-1])
        text = _codepoint_to_utf8(codepoint)
    else:
        raise NotImplementedError('named HTML entity')

    return fn_escape(text)
