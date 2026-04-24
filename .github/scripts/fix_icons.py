import re, glob

def fix_az_page(html):
    original = html

    # 1. Head style'dan .wa-btn CSS'ini sil
    m = re.search(r'(<style[^>]*>)(.*?)(</style>)', html, re.DOTALL)
    if m:
        style_open, content, style_close = m.group(1), m.group(2), m.group(3)
        # .wa-btn { ... } bloğunu sil
        content = re.sub(r'\.wa-btn\s*\{[^}]*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.wa-btn:hover\s*\{[^}]*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.wa-btn\s+svg\s*\{[^}]*\}', '', content, flags=re.DOTALL)
        # Boş satırları temizle
        content = re.sub(r'\n{3,}', '\n\n', content)
        html = html[:m.start()] + style_open + content + style_close + html[m.end():]

    # 2. Body'deki <a class="wa-btn"> anchor'ını sil
    html = re.sub(
        r'<a[^>]+class=["\']wa-btn["\'][^>]*>.*?</a>',
        '', html, flags=re.DOTALL
    )

    # 3. <!-- Floating WhatsApp + Music Button --> yorumunu sil (temizlik)
    html = re.sub(r'<!--\s*Floating WhatsApp\s*\+\s*Music Button\s*-->', '', html)

    return html

# AZ sayfaları: *paltar-boyasi/index.html
files = list(set(glob.glob("*paltar-boyasi*/index.html") +
                 glob.glob("*paltar-boyasi*/index.html")))
# Daha geniş arama
import os
files = []
for root, dirs, fnames in os.walk("."):
    for f in fnames:
        path = os.path.join(root, f)
        if f == "index.html" and "paltar-boyasi" in path and "/ru/" not in path:
            files.append(path)

files = list(set(files))
print(f"Bulunan AZ dosya sayısı: {len(files)}")

fixed = 0
for path in files:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    original = html

    # Sadece wa-btn olan sayfalara uygula
    if 'class="wa-btn"' in html or "class='wa-btn'" in html:
        html = fix_az_page(html)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        fixed += 1
        print(f"  ✅ Temizlendi: {path}")
    else:
        print(f"  ⏭  Değişiklik yok: {path}")

print(f"\nToplam {fixed} dosya güncellendi.")




