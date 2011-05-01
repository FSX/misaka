# -*- coding: utf8 -*-

import pantyshot

print pantyshot
print pantyshot.render

text = 'This **is** *a* `test`. [Test](http://example.com).'

print

for i in range(20):
    result = pantyshot.render(text)
    print '%r' % result
    print result
    print '-'*80
    print
    result = ''