import os, re, glob

# ── Doğru HTML blokları ──────────────────────────────────────────────────────

WA_HTML = """<!-- FLOATING WHATSAPP -->
<a class="whatsapp-float"
   href="https://wa.me/994554828424?text=Здравствуйте!%20Хочу%20заказать%20краску%20для%20одежды%20Viktoria"
   target="_blank" rel="noopener noreferrer" aria-label="Заказать через WhatsApp">
  <svg viewBox="0 0 48 48" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
    <path fill="#fff" d="M24 4C13 4 4 13 4 24c0 3.6 1 7 2.7 9.9L4 44l10.4-2.7C17.1 43 20.5 44 24 44c11 0 20-9 20-20S35 4 24 4zm0 36c-3.1 0-6.1-.8-8.7-2.4l-.6-.4-6.2 1.6 1.7-6-.4-.6C8.8 30.1 8 27.1 8 24 8 15.2 15.2 8 24 8s16 7.2 16 16-7.2 16-16 16zm8.8-11.8c-.5-.2-2.8-1.4-3.2-1.5-.4-.2-.7-.2-1 .2-.3.5-1.2 1.5-1.5 1.9-.3.3-.5.4-1 .1-.5-.2-2-.7-3.8-2.3-1.4-1.2-2.3-2.8-2.6-3.2-.3-.5 0-.7.2-1 .2-.2.5-.6.7-.9.2-.3.3-.5.4-.8.1-.3 0-.6-.1-.9-.1-.2-1-2.4-1.4-3.3-.4-.9-.7-.7-1-.7h-.9c-.3 0-.8.1-1.2.6-.4.5-1.6 1.6-1.6 3.8s1.7 4.4 1.9 4.7c.2.3 3.3 5.1 8 7.1 1.1.5 2 .8 2.7 1 1.1.3 2.2.3 3 .2.9-.1 2.8-1.1 3.2-2.3.4-1.1.4-2.1.3-2.3-.2-.2-.5-.3-1-.5z"/>
  </svg>
</a>"""

MUSIC_HTML = """<button class="float-music" id="musicBtn" aria-label="Музыка">
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path fill="#fff" d="M12 3v10.55A4 4 0 1 0 14 17V7h4V3h-6z"/>
    </svg>
  </button>"""

# ── Gerekli CSS blokları ──────────────────────────────────────────────────────

WA_CSS = """
    /* WhatsApp float */
    .whatsapp-float{position:fixed;bottom:28px;right:28px;z-index:9999;display:flex;align-items:center;justify-content:center;background:#25D366;text-decoration:none;padding:14px;border-radius:50%;box-shadow:0 4px 20px rgba(37,211,102,0.45);transition:transform 0.2s ease,box-shadow 0.2s ease;animation:waPulse 2.5s ease-in-out infinite;}
    .whatsapp-float:hover{transform:scale(1.1);box-shadow:0 6px 28px rgba(37,211,102,0.6);animation:none;}
    .whatsapp-float svg{width:32px;height:32px;fill:#fff;display:block;}
    @keyframes waPulse{0%,100%{box-shadow:0 4px 20px rgba(37,211,102,0.45);}50%{box-shadow:0 4px 32px rgba(37,211,102,0.75);}}"""

MUSIC_CSS = """
    /* Music float */
    .float-music{position:fixed;bottom:100px;right:28px;z-index:9999;display:flex;align-items:center;justify-content:center;background:rgba(75,0,130,0.85);border:none;padding:12px;border-radius:50%;box-shadow:0 4px 16px rgba(75,0,130,0.5);cursor:pointer;transition:transform 0.2s,box-shadow 0.2s;}
    .float-music:hover{transform:scale(1.1);box-shadow:0 6px 24px rgba(75,0,130,0.7);}
    .float-music svg{width:26px;height:26px;display:block;}"""

# ── Dosyaları bul ─────────────────────────────────────────────────────────────

files = (
    glob.glob("**/*dlya-odejdy*.html", recursive=True) +
    glob.glob("**/*dlya-odezhdy*.html", recursive=True)
)
files = list(set(files))  # tekrar edenleri çıkar
print(f"Bulunan dosya sayısı: {len(files)}")

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # ── 1. Eski WhatsApp bloklarını temizle ──────────────────────────────────
    # <!-- FLOATING WHATSAPP --> yorumuyla başlayan tam bloğu sil
    html = re.sub(
        r'<!--\s*FLOATING WHATSAPP\s*-->.*?</a>',
        '', html, flags=re.DOTALL
    )
    # Yorum olmadan yazılmış eski whatsapp-float anchor bloklarını sil
    html = re.sub(
        r'<a[^>]+class=["\']whatsapp-float["\'][^>]*>.*?</a>',
        '', html, flags=re.DOTALL
    )

    # ── 2. Eski müzik butonlarını temizle ────────────────────────────────────
    html = re.sub(
        r'<button[^>]+class=["\']float-music["\'][^>]*>.*?</button>',
        '', html, flags=re.DOTALL
    )
    # Emoji tabanlı eski müzik ikonları (🔇 🎵 gibi)
    html = re.sub(r'[🎵🎶🔇]\s*', '', html)

    # ── 3. CSS kontrolü & ekleme ─────────────────────────────────────────────
    if 'whatsapp-float' not in html:
        html = html.replace('</style>', WA_CSS + '\n  </style>', 1)

    if 'float-music' not in html:
        html = html.replace('</style>', MUSIC_CSS + '\n  </style>', 1)

    # ── 4. İki ikonu </body> öncesine ekle ───────────────────────────────────
    html = html.replace('</body>', WA_HTML + '\n\n' + MUSIC_HTML + '\n\n</body>')

    # ── 5. Değişiklik varsa kaydet ────────────────────────────────────────────
    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ Güncellendi: {path}")
    else:
        print(f"  ⏭  Değişiklik yok: {path}")

print("Tamamlandı.")
