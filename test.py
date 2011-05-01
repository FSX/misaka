# -*- coding: utf8 -*-

import pantyshot as p

print

text = '''

Tables?

Does ~this~ work?

So? http://example.com/

| ------------- | ------------- |
| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | *Content Cell*  |
| Content Cell  | Content Cell  |
| ------------- | ------------- |

<div>Stripped?</div>

'''

result = p.markdown(
    text,
    p.EXT_TABLES | p.EXT_STRIKETHROUGH,
    p.XHTML_SKIP_HTML | p.XHTML_SMARTYPANTS
)
print result
