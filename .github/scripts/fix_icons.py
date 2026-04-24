import re, glob

# ── Sadece bu 4 şeyi temizle, başka hiçbir şeye dokunma ──────────────────────
# 1. <a class="wa-btn"> — body başındaki CSS'siz whatsapp anchor'ı
# 2. <a class="float-wa"> — ICONS-START dışındaki standalone anchor'lar
# 3. <a class="whatsapp-float"> — eski format
# 4. Body içindeki ikinci <style> bloğu (kırık CSS kalıntısı)

ICONS_START = "<!-- ICONS-START -->"
ICONS_END   = "<!-- ICONS-END -->"

def remove_standalone_anchors(html):
    """ICONS-START dışındaki tüm wa-btn, float-wa, whatsapp-float anchor'larını sil."""

    # ICONS bloğunu geçici olarak koru
    icons_block = ""
    if ICONS_START in html and ICONS_END in html:
        start = html.index(ICONS_START)
        end   = html.index(ICONS_END) + len(ICONS_END)
        icons_block = html[start:end]
        html = html[:start] + "%%ICONS_PLACEHOLDER%%" + html[end:]

    # wa-btn anchor
    html = re.sub(
        r'<a[^>]+class=["\']wa-btn["\'][^>]*>.*?</a>',
        '', html, flags=re.DOTALL
    )
    # float-wa anchor (standalone)
    html = re.sub(
        r'<a[^>]+class=["\'][^"\']*float-wa[^"\']*["\'][^>]*>.*?</a>',
        '', html, flags=re.DOTALL
    )
    # whatsapp-float anchor
    html = re.sub(
        r'<!--\s*FLOATING WHATSAPP\s*-->.*?</a>',
        '', html, flags=re.DOTALL
    )
    html = re.sub(
        r'<a[^>]+class=["\']whatsapp-float["\'][^>]*>.*?</a>',
        '', html, flags=re.DOTALL
    )

    # ICONS bloğunu geri koy
    if icons_block:
        html = html.replace("%%ICONS_PLACEHOLDER%%", icons_block)

    return html


def remove_broken_style_blocks(html):
    """Body içindeki kırık/kalıntı <style> bloklarını sil.
    Yalnızca float-wa, float-music, whatsapp-float içeren body <style> bloklarını hedef al.
    <head> içindeki ana <style> bloğuna dokunma.
    """
    # head bloğunu geçici koru
    head_match = re.search(r'<head[^>]*>.*?</head>', html, re.DOTALL)
    head_block = ""
    if head_match:
        head_block = head_match.group(0)
        html = html[:head_match.start()] + "%%HEAD_PLACEHOLDER%%" + html[head_match.end():]

    # Body içindeki kırık style bloklarını sil
    # (float-wa veya float-music veya whatsapp-float içerenler)
    html = re.sub(
        r'<style[^>]*>\s*(?:\.float-wa|\.float-music|\.whatsapp-float|\.wa-btn).*?</style>',
        '', html, flags=re.DOTALL
    )

    # Head'i geri koy
    if head_block:
        html = html.replace("%%HEAD_PLACEHOLDER%%", head_block)

    return html


# ── Dosyaları bul ─────────────────────────────────────────────────────────────
files = list(set(
    glob.glob("ru/*dlya-odejdy*/index.html") +
    glob.glob("ru/*dlya-odezhdy*/index.html")
))
print(f"Bulunan dosya sayısı: {len(files)}")

fixed = 0
for path in files:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    original = html

    html = remove_standalone_anchors(html)
    html = remove_broken_style_blocks(html)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        fixed += 1
        print(f"  ✅ Temizlendi: {path}")

print(f"\nToplam {fixed} dosya güncellendi.")
print("Tamamlandı.")



