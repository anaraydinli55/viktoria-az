import os, re, glob

# Dəyişdiriləcək pattern → yeni dəyər
REPLACEMENTS = [
    # href="...catalog.html"  →  href="/catalog"
    (r'href="([^"]*?)catalog\.html"',    lambda m: f'href="{m.group(1).rstrip("/")}catalog"' if m.group(1) else 'href="/catalog"'),
    # href='...catalog.html'  →  href='/catalog'
    (r"href='([^']*?)catalog\.html'",    lambda m: f"href='{m.group(1).rstrip('/')}catalog'" if m.group(1) else "href='/catalog'"),
]

# Tüm HTML dosyalarını bul (ru/ dahil, .github/ hariç)
files = []
for root, dirs, fnames in os.walk("."):
    # .github, node_modules, .git klasörlerini atla
    dirs[:] = [d for d in dirs if d not in {'.git', '.github', 'node_modules'}]
    for f in fnames:
        if f.endswith(".html"):
            files.append(os.path.join(root, f))

print(f"Toplam HTML dosya sayısı: {len(files)}")

fixed = 0
for path in files:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    original = html

    # catalog.html → /catalog
    html = re.sub(
        r'(href=["\'])([^"\']*?)catalog\.html(["\'])',
        lambda m: m.group(1) + (m.group(2).rstrip('/') or '/') + 'catalog' + m.group(3),
        html
    )

    # /www.viktoria-az.store/catalog.html → /www.viktoria-az.store/catalog
    # Zaten üstteki regex bunu da kapsıyor

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        fixed += 1
        print(f"  ✅ Güncellendi: {path}")

print(f"\nToplam {fixed} dosya güncellendi.")
