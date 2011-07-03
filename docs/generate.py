import misaka as m

if __name__ == '__main__':
    with open('./documentation.md', 'r') as fd:
        src =  fd.read().strip()

    html = m.html(src, m.EXT_AUTOLINK, m.HTML_TOC)
    toc = m.toc(src)

    with open('template.html', 'r') as fd:
        tpl = fd.read().strip()

    tpl = tpl.replace('{{ navigation }}', toc, 1)
    tpl = tpl.replace('{{ content }}', html, 1)

    with open('index.html', 'w') as fd:
        fd.write(tpl)