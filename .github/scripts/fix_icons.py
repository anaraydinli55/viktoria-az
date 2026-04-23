import re, glob

# ── Doğru HTML + JS ───────────────────────────────────────────────────────────
ICONS_START = "<!-- ICONS-START -->"
ICONS_END   = "<!-- ICONS-END -->"

NEW_HTML = ICONS_START + """
<audio id="bgMusic" src="/music/musiqi.mpeg" preload="auto" loop></audio>
<div class="float-group">
  <button id="musicBtn" class="float-btn float-music" aria-label="Play Music">
    <svg viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>
  </button>
  <a href="https://wa.me/994554828424?text=Здравствуйте!%20Хочу%20заказать%20краску%20для%20одежды%20Viktoria" class="float-btn float-wa" target="_blank" rel="noopener">
    <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.414 0 .004 5.411.001 12.045a11.811 11.811 0 001.592 5.96L0 24l6.117-1.605a11.772 11.772 0 005.925 1.585h.005c6.637 0 12.046-5.411 12.049-12.047a11.814 11.814 0 00-3.576-8.504"/></svg>
  </a>
</div>
<script>
  const music = document.getElementById("bgMusic");
  const musicBtn = document.getElementById("musicBtn");
  let started = false, playing = false;
  function toggleMusic() {
    if (!started) {
      music.volume = 0.4;
      music.play().then(() => { started = true; playing = true; musicBtn.classList.add("playing"); }).catch(e => console.log(e));
    } else {
      if (playing) { music.pause(); playing = false; musicBtn.classList.remove("playing"); }
      else { music.play(); playing = true; musicBtn.classList.add("playing"); }
    }
  }
  window.addEventListener("scroll", () => { if(!started) toggleMusic(); }, { once: true });
  musicBtn.addEventListener("click", toggleMusic);
</script>
""" + ICONS_END

# ── Doğru CSS ─────────────────────────────────────────────────────────────────
CLEAN_FLOAT_CSS = """    /* FLOATING BUTTONS */
    .float-group{position:fixed;bottom:22px;right:20px;display:flex;flex-direction:column;align-items:center;gap:12px;z-index:9999;}
    .float-btn{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;text-decoration:none;cursor:pointer;border:none;transition:all 0.3s cubic-bezier(0.34,1.56,0.64,1);box-shadow:0 4px 18px rgba(0,0,0,0.25);}
    .float-btn:hover{transform:scale(1.12);}
    .float-wa{background:linear-gradient(135deg,#25D366,#1cb554);}
    .float-music{background:#4b0082;}
    .float-btn svg{width:30px;height:30px;fill:#fff;}
    .playing{animation:musicPulse 1.8s ease-in-out infinite;}
    @keyframes musicPulse{0%,100%{box-shadow:0 4px 18px rgba(75,0,130,0.38);}50%{box-shadow:0 4px 30px rgba(75,0,130,0.75);}}"""

def fix_style(html):
    """Style bloğundaki tüm icon CSS'ini temizleyip doğru olanı ekle."""
    m = re.search(r'(<style[^>]*>)(.*?)(</style>)', html, re.DOTALL)
    if not m:
        # Style yok, head'e ekle
        return html.replace('</head>', '<style>\n' + CLEAN_FLOAT_CSS + '\n</style>\n</head>', 1)

    style_open, content, style_close = m.group(1), m.group(2), m.group(3)

    # Satır satır tara, icon ile ilgili satırları çıkar
    bad_keywords = [
        'float-group', 'float-btn', 'float-wa', 'float-music',
        'whatsapp-float', 'waPulse', 'musicPulse', 'wa-btn',
        'ICONS-CSS', 'FLOATING BUTTONS', 'playing',
        '.playing', '25D366', '1cb554',
    ]
    # Ayrıca kırık orphan satırları temizle
    # "50%{box-shadow:..." gibi
    orphan_patterns = [
        r'^\s*50%\{box-shadow:[^}]*\}\}?\s*$',
        r'^\s*\.wa-btn\s*,\s*\.float-wa\s*,\s*$',
        r'^\s*$',  # sadece boş satır — aşağıda kontrol edilecek
    ]

    lines = content.split('\n')
    clean = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Kötü keyword içeriyor mu?
        if any(kw in line for kw in bad_keywords):
            # Bu satırı ve devamındaki bloğu atla
            # Eğer { varsa kapanış } 'e kadar atla
            if '{' in line and '}' not in line:
                depth = line.count('{') - line.count('}')
                i += 1
                while i < len(lines) and depth > 0:
                    depth += lines[i].count('{') - lines[i].count('}')
                    i += 1
                continue
            else:
                i += 1
                continue
        # Orphan satır mı?
        is_orphan = False
        for pat in orphan_patterns[:2]:  # boş satır hariç
            if re.match(pat, line):
                is_orphan = True
                break
        if is_orphan:
            i += 1
            continue
        clean.append(line)
        i += 1

    # Fazla boş satırları temizle
    clean_content = re.sub(r'\n{3,}', '\n\n', '\n'.join(clean))

    new_style = style_open + clean_content + '\n' + CLEAN_FLOAT_CSS + '\n  ' + style_close
    return html[:m.start()] + new_style + html[m.end():]


def fix_html_body(html):
    """Body'deki eski icon HTML'lerini temizleyip doğruyu ekle."""

    # 1. ICONS marker arasını sil
    html = re.sub(
        re.escape(ICONS_START) + r'.*?' + re.escape(ICONS_END),
        '', html, flags=re.DOTALL
    )

# float-group dışındaki tüm float-wa anchor'larını sil
html = re.sub(
    r'<a[^>]+class=["\'][^"\']*float-wa[^"\']*["\'][^>]*>.*?</a>',
    '', html, flags=re.DOTALL
)
# Eski whatsapp-float anchor (farklı class formatı)
html = re.sub(
    r'<a[^>]+(?:float-wa|whatsapp-float)[^>]*>.*?</a>',
    '', html, flags=re.DOTALL
)

    # 3. Eski whatsapp-float anchor'ı sil
    html = re.sub(
        r'<!--\s*FLOATING WHATSAPP\s*-->.*?</a>',
        '', html, flags=re.DOTALL
    )
    html = re.sub(
        r'<a[^>]+class=["\']whatsapp-float["\'][^>]*>.*?</a>',
        '', html, flags=re.DOTALL
    )

    # 4. Eski float-group div'ini sil (içinde musicBtn var)
    # Nested div'leri doğru saymak için manuel parse
    pattern = r'<div[^>]+class=["\']float-group["\'][^>]*>'
    while True:
        m = re.search(pattern, html)
        if not m:
            break
        start = m.start()
        pos = m.end()
        depth = 1
        while pos < len(html) and depth > 0:
            next_open  = html.find('<div', pos)
            next_close = html.find('</div>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                pos = next_close + 6
        html = html[:start] + html[pos:]

    # 5. Eski audio tag'ini sil
    html = re.sub(r'<audio[^>]+bgMusic[^>]*>(?:.*?</audio>)?', '', html, flags=re.DOTALL)
    html = re.sub(r'<audio[^>]+bgMusic[^>]*/>', '', html, flags=re.DOTALL)

    # 6. Eski müzik JS bloğunu sil
    html = re.sub(r'<script>\s*const music\s*=.*?</script>', '', html, flags=re.DOTALL)

    # 7. Eski tek float-music button'ı sil
    html = re.sub(r'<button[^>]+float-music[^>]*>.*?</button>', '', html, flags=re.DOTALL)

    # 8. Eski yorum satırları
    html = re.sub(r'<!--\s*Music Button[^>]*-->', '', html, flags=re.DOTALL)

    # 9. Emoji
    html = re.sub(r'[🎵🎶🔇]\s*', '', html)

    # 10. Yeni bloğu </body> öncesine ekle
    html = html.replace('</body>', NEW_HTML + '\n</body>')

    return html


# ── Dosyaları bul ─────────────────────────────────────────────────────────────
files = list(set(
    glob.glob("ru/*dlya-odejdy*/index.html") +
    glob.glob("ru/*dlya-odezhdy*/index.html")
))
print(f"Bulunan dosya sayısı: {len(files)}")

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    original = html

    html = fix_style(html)
    html = fix_html_body(html)
    html = re.sub(r'\n{4,}', '\n\n', html)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ Güncellendi: {path}")
    else:
        print(f"  ⏭  Değişiklik yok: {path}")

print("Tamamlandı.")

