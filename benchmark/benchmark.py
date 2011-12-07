import time
import os.path as path


modules = {}
names = ('misaka', 'markdown', 'markdown2', 'cMarkdown', 'discount')
for name in names:
    try:
        modules[name] = __import__(name)
    except ImportError:
        pass


rndr = modules['misaka'].HtmlRenderer()
m = modules['misaka'].Markdown(rndr)


class Benchmark(object):
    def __init__(self, name):
        self._name = name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = time.clock()
            func(*args, **kwargs)
            end = time.clock()
            return end - start
        wrapper.__name__ = func.__name__
        return wrapper


@Benchmark('Misaka')
def benchmark_misaka(text):
    modules['misaka'].html(text)


@Benchmark('Misaka (classes)')
def benchmark_misaka_classes(text):
    m.render(text)


@Benchmark('markdown2')
def benchmark_markdown2(text):
    modules['markdown2'].markdown(text)


@Benchmark('Markdown')
def benchmark_markdown(text):
    modules['markdown'].markdown(text)


@Benchmark('cMarkdown')
def benchmark_cMarkdown(text):
    modules['cMarkdown'].markdown(text)


@Benchmark('discount')
def benchmark_discount(text):
    modules['discount'].Markdown(text).get_html_content()


if __name__ == '__main__':
    with open(path.join(path.dirname(__file__), 'markdown-syntax.md'), 'r') as fd:
        text = fd.read()

    loops = 10000
    totals = []
    methods = [
        ('Misaka', benchmark_misaka),
        ('Misaka (classes)', benchmark_misaka_classes),
        ('Markdown', benchmark_markdown),
        ('Markdown2', benchmark_markdown2),
        ('cMarkdown', benchmark_cMarkdown),
        ('Discount', benchmark_discount)
    ]

    print('Parsing the Markdown Syntax document %d times...' % loops)

    for i, method in enumerate(methods):
        name = method[1].__name__.split('_', 2)[1]
        if name not in modules:
            print('%s is not available' % method[0])
            continue
        total = 0
        for nth in range(0, loops):
            total += method[1](text)
        print('%s: %gs' % (method[0], total))
