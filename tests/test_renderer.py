# -*- coding: utf-8 -*-

import misaka as m
from chibitest import TestCase, ok


class TestRenderer(m.BaseRenderer):
    def blockcode(self, text, language):
        return '[BLOCK_CODE language={1}] {0}'.format(text, language)

    def paragraph(self, text):
        return '[PARAGRAPH] {0}\n'.format(text)

    def normal_text(self, text):
        return text


class CustomRendererTest(TestCase):
    name = 'Custom Renderer'

    def setup(self):
        self.renderer = TestRenderer()
        self.render = m.Markdown(TestRenderer(), m.EXT_FENCED_CODE).render

    def test_block_code(self):
        supplied = '```bash\n$ :(){ :|:& };:\n```'
        expected = '[BLOCK_CODE language=bash] $ :(){ :|:& };:\n'

        ok(self.render(supplied)).diff(expected)
