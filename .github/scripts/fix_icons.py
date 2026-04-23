import os, re, glob

# ── Doğru CSS ────────────────────────────────────────────────────────────────

NEW_CSS = """
    /* FLOATING BUTTONS */
    .float-group {
      position: fixed;
      bottom: 22px;
      right: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
      z-index: 9999;
    }
    .float-btn {
      width: 56px;
      height: 56px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      cursor: pointer;
      border: none;
      transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
      box-shadow: 0 4px 18px rgba(0,0,0,0.25);
    }
    .float-btn:hover { transform: scale(1.12); }
    .float-wa { background: linear-gradient(135deg, #25D366, #1cb554); }
    .float-music { background: #4b0082; }
    .float-btn svg { width: 30px; height: 30px; fill: #fff; }
    .playing { animation: musicPulse 1.8s ease-in-out infinite; }
    @keyframes musicPulse {
      0%, 100% { box-shadow: 0 4px 18px rgba(75, 0, 130, 0.38); }
      50% { box-shadow: 0 4px 30px rgba(75, 0, 130, 0.75); }
    }"""

# ── Doğru HTML + JS ───────────────────────────────────────────────────────────

NEW_BODY = """<audio id="bgMusic" src="/music/musiqi.mpeg" preload="auto" loop></audio>
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
    let started = false;
    let playing = false;
    function toggleMusic() {
      if (!started) {
        music.volume = 0.4;
        music.play().then(() => {
          started = true;
          playing = true;
          musicBtn.classList.add("playing");
        }).catch(e => console.log("Hata:", e));
      } else {
        if (playing) {
          music.pause();
          playing = false;
          musicBtn.classList.remove("playing");
        } else {
          music.play();
          playing = true;
          musicBtn.classList.add("playing");
        }
      }
    }
    window.addEventListener("scroll", () => { if(!started) toggleMusic(); }, { once: true });
    musicBtn.addEventListener("click", toggleMusic);
  </script>"""

# ── Temizlenecek CSS pattern'leri ─────────────────────────────────────────────

CSS_PATTERNS = [
    r'/\*\s*WhatsApp float\s*\*/.*?(?=\n\s*[.#a-zA-Z@]|\n\s*</style>)',
    r'/\*\s*Music float\s*\*/.*?(?=\n\s*[.#a-zA-Z@]|\n\s*</style>)',
    r'/\*\s*FLOATING BUTTONS\s*\*/.*?(?=\n\s*</style>)',
    r'@keyframes waPulse\s*\{[^}]*\}',
    r'@keyframes musicPulse\s*\{[^}]*\}',
    r'\.float-group\s*\{[^}]*\}',
    r'\.float-btn\s*\{[^}]*\}',
    r'\.float-btn:hover\s*\{[^}]*\}',
    r'\.float-wa\s*\{[^}]*\}',
    r'\.float-music\s*\{[^}]*\}',
    r'\.float-btn\s+svg\s*\{[^}]*\}',
    r'\.playing\s*\{[^}]*\}',
    r'\.whatsapp-float[^{]*\{[^}]*\}',
    r'\.whatsapp-float:hover[^{]*\{[^}]*\}',
    r'\.whatsapp-float\s+svg[^{]*\{[^}]*\}',
]

# ── Temizlenecek HTML pattern'leri ────────────────────────────────────────────

HTML_PATTERNS = [
    r'<!--\s*FLOATING WHATSAPP\s*-->.*?</a>',
    r'<a[^>]+class=["\']whatsapp-float["\'][^>]*>.*?</a>',
    r'<button[^>]+class=["\']float-music["\'][^>]*>.*?</button>',
    r'<div[^>]+class=["\']float-group["\'][^>]*>.*?</div>',
    r'<audio[^>]+id=["\']bgMusic["\'][^>]*>.*?</audio>',
    r'<audio[^>]+id=["\']bgMusic["\'][^>]*/>',
    r'<audio[^>]+id=["\']bgMusic["\'][^>]*>',
    r'<script>\s*const music\s*=.*?</script>',
    r'[🎵🎶🔇]\s*',
]

# ── Dosyaları bul ─────────────────────────────────────────────────────────────

files = (
    glob.glob("ru/*dlya-odejdy*/index.html") +
    glob.glob("ru/*dlya-odezhdy*/index.html")
)
files = list(set(files))
print(f"Bulunan dosya sayısı: {len(files)}")

for path in files:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # 1. Eski CSS temizle
    for pattern in CSS_PATTERNS:
        html = re.sub(pattern, '', html, flags=re.DOTALL | re.IGNORECASE)

    # 2. Eski HTML temizle
    for pattern in HTML_PATTERNS:
        html = re.sub(pattern, '', html, flags=re.DOTALL | re.IGNORECASE)

    # 3. Boş satırları temizle
    html = re.sub(r'\n{3,}', '\n\n', html)

    # 4. Yeni CSS ekle (</style> öncesine, sadece yoksa)
    if 'float-group' not in html:
        html = html.replace('</style>', NEW_CSS + '\n  </style>', 1)

    # 5. Yeni HTML + JS ekle (</body> öncesine)
    html = html.replace('</body>', NEW_BODY + '\n</body>')

    # 6. Kaydet
    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ Güncellendi: {path}")
    else:
        print(f"  ⏭  Değişiklik yok: {path}")

print("Tamamlandı.")

