import time

import misaka
import markdown
import markdown2
import cMarkdown
import discount


class Benchmark(object):
    def __init__(self, name):
        self._name = name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = time.clock()
            func(*args, **kwargs)
            end = time.clock()
            return end - start
        return wrapper


@Benchmark('Misaka')
def benchmark_misaka(text):
    misaka.html(text)


@Benchmark('markdown2')
def benchmark_markdown2(text):
    markdown2.markdown(text)


@Benchmark('Markdown')
def benchmark_markdown(text):
    markdown.markdown(text)


@Benchmark('cMarkdown')
def benchmark_cmarkdown(text):
    cMarkdown.markdown(text)


@Benchmark('discount')
def benchmark_discount(text):
    discount.Markdown(text).get_html_content()


if __name__ == '__main__':
    with open('markdown-syntax.md', 'r') as fd:
        text = fd.read()

    loops = 10000
    totals = []
    methods = [
        ('Misaka', benchmark_misaka),
        ('Markdown', benchmark_markdown),
        ('Markdown2', benchmark_markdown2),
        ('cMarkdown', benchmark_cmarkdown),
        ('Discount', benchmark_discount)
    ]

    print 'Parsing the Markdown Syntax document %s times...' % loops

    for i, method in enumerate(methods):
        total = 0
        for nth in range(0, loops):
            total += method[1](text)
        print '%s: %gs' % (method[0], total)
