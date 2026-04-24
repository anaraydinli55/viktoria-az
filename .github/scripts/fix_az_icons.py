import re, glob, os

NEW_WA_SVG = '<svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.414 0 .004 5.411.001 12.045a11.811 11.811 0 001.592 5.96L0 24l6.117-1.605a11.772 11.772 0 005.925 1.585h.005c6.637 0 12.046-5.411 12.049-12.047a11.814 11.814 0 00-3.576-8.504"/></svg>'

def fix_az_page(html):
    # 1. Head style'dan .wa-btn CSS'ini sil
    m = re.search(r'(<style[^>]*>)(.*?)(</style>)', html, re.DOTALL)
    if m:
        style_open, content, style_close = m.group(1), m.group(2), m.group(3)
        content = re.sub(r'\.wa-btn\s*\{[^}]*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.wa-btn:hover\s*\{[^}]*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.wa-btn\s+svg\s*\{[^}]*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\n{3,}', '\n\n', content)
        html = html[:m.start()] + style_open + content + style_close + html[m.end():]

    # 2. <a class="wa-btn"> anchor'ını sil
    html = re.sub(
        r'<a[^>]+class=["\']wa-btn["\'][^>]*>.*?</a>',
        '', html, flags=re.DOTALL
    )

    # 3. Yorum satırını temizle
    html = re.sub(r'<!--\s*Floating WhatsApp.*?-->', '', html)

    # 4. float-wa içindeki SVG'yi yeni SVG ile değiştir
    html = re.sub(
        r'(<a[^>]+class=["\'][^"\']*float-wa[^"\']*["\'][^>]*>)\s*<svg[\s\S]*?</svg>\s*(</a>)',
        r'\g<1>' + NEW_WA_SVG + r'\g<2>',
        html, flags=re.DOTALL
    )

    return html


# AZ sayfaları: paltar-boyasi içeren, /ru/ olmayan
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

    html = fix_az_page(html)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        fixed += 1
        print(f"  ✅ Temizlendi: {path}")
    else:
        print(f"  ⏭  Değişiklik yok: {path}")

print(f"\nToplam {fixed} dosya güncellendi.")

