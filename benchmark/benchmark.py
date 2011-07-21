import time


try:
    import misaka
except ImportError:
    misaka = None
    print('misaka is not available...')

try:
    import markdown
except ImportError:
    markdown = None
    print('Markdown is not available...')

try:
    import markdown2
except ImportError:
    markdown2 = None
    print('markdown2 is not available...')

try:
    import cMarkdown
except ImportError:
    cMarkdown = None
    print('cMarkdown is not available...')

try:
    import discount
except ImportError:
    discount = None
    print('discount is not available...')


class Benchmark(object):
    def __init__(self, name):
        self._name = name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = time.clock()
            func(*args, **kwargs)
            end = time.clock()
            print('%s: %fs' % (self._name, end - start))
        return wrapper


@Benchmark('misaka')
def benchmark_misaka(text, loops):
    for i in loops:
        misaka.html(text)


@Benchmark('markdown2')
def benchmark_markdown2(text, loops):
    for i in loops:
        markdown2.markdown(text)


@Benchmark('Markdown')
def benchmark_markdown(text, loops):
    for i in loops:
        markdown.markdown(text)


@Benchmark('cMarkdown')
def benchmark_cmarkdown(text, loops):
    for i in loops:
        cMarkdown.markdown(text)


@Benchmark('discount')
def benchmark_discount(text, loops):
    for i in loops:
        discount.Markdown(text).get_html_content()


if __name__ == '__main__':
    with open('markdown-syntax.md', 'r') as fd:
        text = fd.read()

    loops = range(0, 100)

    if misaka:
        benchmark_misaka(text, loops)
    if markdown:
        benchmark_markdown(text, loops)
    if markdown2:
        benchmark_markdown2(text, loops)
    if cMarkdown:
        benchmark_cmarkdown(text, loops)
    if discount:
        benchmark_discount(text, loops)
