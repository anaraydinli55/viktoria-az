import re, os

CATALOG_FILE = "ru/catalog/index.html"

# Görsel → RU ürün sayfası tam mapping
IMAGE_LINK_MAP = {
    "1-pembe.webp":         "/ru/viktoria-rozovaya-kraska-dlya-odejdy",
    "2-kavunici.webp":      "/ru/viktoria-dynniy-kraska-dlya-odejdy",
    "3-yavruagzi.webp":     "/ru/viktoria-persikoviy-kraska-dlya-odejdy",
    "4-koyu-pembe.webp":    "/ru/viktoria-temno-rozovaya-kraska-dlya-odejdy",
    "5-al.webp":            "/ru/viktoria-aliy-krasniy-kraska-dlya-odejdy",
    "6-atresi-pembe.webp":  "/ru/viktoria-ognenno-rozovaya-kraska-dlya-odejdy",
    "7-nar-cicegi.webp":    "/ru/viktoria-tsvetok-granata-kraska-dlya-odejdy",
    "8-kirmizi.webp":       "/ru/viktoria-krasnaya-kraska-dlya-odejdy",
    "9-koyu-kirmizi.webp":  "/ru/viktoria-temno-krasniy-kraska-dlya-odejdy",
    "10-visne-curugu.webp": "/ru/viktoria-vyshnevo-krasniy-kraska-dlya-odejdy",
    "11-sari.webp":         "/ru/viktoria-jeltaya-kraska-dlya-odejdy",
    "12-turuncu.webp":      "/ru/viktoria-oranjevaya-kraska-dlya-odejdy",
    "13-gul-kurusu.webp":   "/ru/viktoria-pylnaya-roza-kraska-dlya-odejdy",
    "14-bej-acik.webp":     "/ru/viktoria-svetlo-bejeviy-kraska-dlya-odejdy",
    "15-bej-koyu.webp":     "/ru/viktoria-temno-bej-kraska-dlya-odezhdy",
    "16-tutun-rengi.webp":  "/ru/viktoria-tabachniy-kraska-dlya-odejdy",
    "17-acik-kahve.webp":   "/ru/viktoria-svetlo-korichnevaya-kraska-dlya-odezhdy",
    "18-kahve-orta.webp":   "/ru/viktoria-sredne-korichnevaya-kraska-dlya-odejdy",
    "19-kahve.webp":        "/ru/viktoria-korichnevaya-kraska-dlya-odejdy",
    "20-kahve-koyu.webp":   "/ru/viktoria-temno-korichnevaya-kraska-dlya-odejdy",
    "21-fes-rengi.webp":    "/ru/viktoria-bordovaya-kraska-dlya-odejdy",
    "22-guvez.webp":        "/ru/viktoria-bordoviy-ksrasniy-kraska-dlya-odejdy",
    "23-acik-mavi.webp":    "/ru/viktoria-golubaia-kraska-dlya-odejdy",
    "24-mavi-orta.webp":    "/ru/viktoria-sredne-sinyaya-kraska-dlya-odejdy",
    "25-mavi-koyu.webp":    "/ru/viktoria-temno-sinyaya-kraska-dlya-odejdy",
    "26-mor-acik.webp":     "/ru/viktoria-svetlo-fioletovaya-kraska-dlya-odejdy",
    "27-mor-koyu.webp":     "/ru/viktoria-temno-fioletovaya-kraska-dlya-odejdy",
    "28-lacivert-acik.webp":"/ru/viktoria-golubaya-kraska-dlya-odejdy",
    "29-lacivert-orta.webp":"/ru/viktoria-sredne-siniy-kraska-dlya-odezhdy",
    "30-siyah.webp":        "/ru/viktoria-chernaya-kraska-dlya-odejdy",
    "31-eflatun.webp":      "/ru/viktoria-purpurniy-kraska-dlya-odejdy",
    "32-bej.webp":          "/ru/viktoria-bejeviy-kraska-dlya-odejdy",
    "33-kursuni-acik.webp": "/ru/viktoria-svetlo-seraya-kraska-dlya-odejdy",
    "34-kursuni-koyu.webp": "/ru/viktoria-temno-seraya-kraska-dlya-odejdy",
    "35-cam-gobegi.webp":   "/ru/viktoria-tsvet-morskoj-volny-kraska-dlya-odejdy",
    "36-filizi-acik.webp":  "/ru/viktoria-svetlo-salatoviy-kraska-dlya-odejdy",
    "37-filizi-koyu.webp":  "/ru/viktoria-temno-salatoviy-kraska-dlya-odezhdy",
    "38-yesil.webp":        "/ru/viktoria-zelenaya-kraska-dlya-odejdy",
    "39-koyu-yesil.webp":   "/ru/viktoria-temno-zelyonaya-kraska-dlya-odezhdy",
    "40-nefti.webp":        "/ru/viktoria-neftyanoy-kraska-dlya-odejdy",
    "41-haki.webp":         "/ru/viktoria-haki-kraska-dlya-odejdy",
    "42-kanarya.webp":      "/ru/viktoria-kanareechniy-kraska-dlya-odejdy",
    "43-sarabi.webp":       "/ru/viktoria-marsala-kraska-dlya-odejdy",
    "44-portakal.webp":     "/ru/viktoria-apelsinoviy-kraska-dlya-odejdy",
    "45-zumrut.webp":       "/ru/viktoria-izumrudniy-kraska-dlya-odejdy",
    "46-petrol.webp":       "/ru/viktoria-petrol-kraska-dlya-odejdy",
    "47-zeytini.webp":      "/ru/viktoria-olivkoviy-kraska-dlya-odejdy",
    "48-saksonya.webp":     "/ru/viktoria-indigo-kraska-dlya-odejdy",
    "49-civit-mavi.webp":   "/ru/viktoria-indigo-kraska-dlya-odejdy",
    "50-m-lacivert.webp":   "/ru/viktoria-sine-fioletovaya-kraska-dlya-odejdy",
    "51-lacivert-koyu.webp":"/ru/viktoria-temno-golubaya-kraska-dlya-odejdy",
    "52-yanik-kahve.webp":  "/ru/viktoria-jjenniy-korichneviy-kraska-dlya-odejdy",
    "53-sarabi-koyu.webp":  "/ru/viktoria-temnaya-marsala-kraska-dlya-odejdy",
    "54-eflatun-koyu.webp": "/ru/viktoria-temno-purpurniy-lavanda-kraska-dlya-odejdy",
    "55-menekse.webp":      "/ru/viktoria-fioletovaya-kraska-dlya-odejdy",
    "56-altin-sari.webp":   "/ru/viktoria-zolotisto-jeltaya-kraska-dlya-odejdy",
    "57-k-sari.webp":       "/ru/viktoria-temno-jeltaya-kraska-dlya-odejdy",
    "60-boncuk-mavi.webp":  "/ru/viktoria-biryuzovaya-kraska-dlya-odezhdy",
    "61-blujin-mavisi.webp":"/ru/viktoria-dzhinsovyy-siniy-kraska-dlya-odezhdy",
    "62-fiske.webp":        "/ru/viktoria-zakrepitel-cveta-kraski-dlya-odezhdy",
}

if not os.path.exists(CATALOG_FILE):
    print(f"Fayl tapılmadı: {CATALOG_FILE}")
    exit(1)

with open(CATALOG_FILE, "r", encoding="utf-8") as f:
    html = f.read()

original = html

# 1. img.onclick satırını c.link kullanan versiyona güncelle
html = re.sub(
    r'img\.onclick\s*=\s*\(\)\s*=>\s*window\.location\.href\s*=\s*[^;]+;',
    'img.onclick = () => window.location.href = c.link || "/ru/catalog";',
    html
)

# 2. colors dizisindeki her {file:"X.webp", color:"Y"} objesine link ekle
def add_link(m):
    obj = m.group(0)
    file_match = re.search(r'file:"([^"]+)"', obj)
    if not file_match:
        return obj
    filename = file_match.group(1)
    if 'link:' in obj:
        # Zaten link var, sadece doğru olanla değiştir
        if filename in IMAGE_LINK_MAP:
            obj = re.sub(r'link:"[^"]*"', f'link:"{IMAGE_LINK_MAP[filename]}"', obj)
        return obj
    if filename in IMAGE_LINK_MAP:
        # Kapanış } öncesine link ekle
        obj = obj.rstrip('}').rstrip() + f', link:"{IMAGE_LINK_MAP[filename]}"}}'
    return obj

html = re.sub(
    r'\{file:"[^"]+\.webp"[^}]+\}',
    add_link,
    html
)

if html != original:
    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {CATALOG_FILE} güncellendi.")
else:
    print(f"⏭  Değişiklik yok: {CATALOG_FILE}")
