# -*- coding: utf-8 -*-
# sitemap.xml-dən mövcud olmayan səhifələri silir (GitHub Actions + lokal)
import os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
BASE = 'https://viktoria-az.store'


def exists(path):
    p = path.strip('/')
    return p == '' or os.path.isfile(p) or os.path.isfile(p + '.html') or os.path.isfile(os.path.join(p, 'index.html'))


def main():
    os.chdir(ROOT)
    raw = open('sitemap.xml', encoding='utf-8', newline='').read()
    removed = []

    def keep(m):
        loc = re.search(r'<loc>([^<]+)</loc>', m.group(0))
        if loc and loc.group(1).startswith(BASE) and not exists(loc.group(1)[len(BASE):]):
            removed.append(loc.group(1))
            return ''
        return m.group(0)
    new = re.sub(r'[ \t]*<url>.*?</url>[ \t]*\r?\n?', keep, raw, flags=re.S)
    if new != raw:
        open('sitemap.xml', 'w', encoding='utf-8', newline='').write(new)
    print('sitemap: %d mövcud olmayan URL silindi' % len(removed))
    for u in removed:
        print('  -', u)


if __name__ == '__main__':
    main()
